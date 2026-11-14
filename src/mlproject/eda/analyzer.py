import pandas as pd
import numpy as np

from typing import Any

from mlproject.data import get_columns_config, load_dataset, validate_columns
from mlproject.eda.schemas import (
  DatasetProfiling,
  DatasetStructure, CategoricalDistribution, CategoryFrequency, MissingValueInfo, DataQuality, ColumnDistribution,
  DistributionStats, HistogramData
)


def _dataset_structure(df: pd.DataFrame) -> DatasetStructure:
  return DatasetStructure(
    n_rows=len(df),
    n_columns=len(df.columns),
    memory_mb=round(
      df.memory_usage(deep=True).sum() / 1024 ** 2,
      2
    ),
    columns=df.columns
  )


def _analyze_constraints(
  df: pd.DataFrame,
  config: dict,
) -> dict[str, dict[str, int]]:
  results = {}

  for column, settings in get_columns_config(config).items():
    if column not in df.columns:
      continue

    constraints = settings.get("constraints", {})

    if not constraints:
      continue

    violations = {}

    if "min" in constraints or "max" in constraints:
      values = pd.to_numeric(
        df[column],
        errors="coerce",
      )

      if "min" in constraints:
        violations["below_min"] = int(
          (values.notna() & (values < constraints["min"])).sum()
        )

      if "max" in constraints:
        violations["above_max"] = int(
          (values.notna() & (values > constraints["max"])).sum()
        )

      if constraints.get("integer"):
        violations["non_integer"] = int(
          (values.notna() & (values % 1 != 0)).sum()
        )

    results[column] = violations

  return results

def _dataset_quality(df: pd.DataFrame, config: dict) -> DataQuality:
  missing_values: list[MissingValueInfo] = []

  for column in df.columns:
    missing_count = df[column].isnull().sum()
    missing_percent = df[column].isnull().mean() * 100

    missing_values.append(
      MissingValueInfo(
        column=column,
        missing_count=int(missing_count),
        missing_percentage=float(missing_percent),
      )
    )

  constant_columns = [
    col for col in df.columns
    if df[col].nunique(dropna=False) <= 1
  ]
  return DataQuality(
    duplicate_rows=int(df.duplicated().sum()),
    duplicate_percentage=df.duplicated().sum() / len(df) * 100,
    missing_values=missing_values,
    constant_columns=constant_columns,
    constraint_violations=_analyze_constraints(df, config)
  )

def _column_distribution(series: pd.Series) -> ColumnDistribution:
  clean = series.dropna()
  stats = DistributionStats(
    count=int(clean.count()),
    unique=int(clean.nunique())
  )

  if pd.api.types.is_numeric_dtype(clean):
    stats.min = float(clean.min()) if not clean.empty else None
    stats.max = float(clean.max()) if not clean.empty else None
    stats.mean = float(clean.mean()) if not clean.empty else None
    stats.median = float(clean.median()) if not clean.empty else None
    stats.std = float(clean.std()) if len(clean) > 1 else None
    stats.q1 = float(clean.quantile(0.25)) if not clean.empty else None
    stats.q3 = float(clean.quantile(0.75)) if not clean.empty else None
    stats.skewness = float(clean.skew()) if len(clean) > 2 else None
    stats.kurtosis = float(clean.kurt()) if len(clean) > 3 else None

  return ColumnDistribution(
    name=str(series.name),
    dtype=str(series.dtype),
    stats=stats
  )

def _dataset_distribution(df: pd.DataFrame) -> dict[str, ColumnDistribution]:
  return {
    col: _column_distribution(df[col]) for col in df.columns
  }

def _dataset_histogram(series: pd.Series, bins: int = 10) -> HistogramData:
  if bins < 1:
    raise ValueError("bins must be greater than zero")

  if not pd.api.types.is_numeric_dtype(series):
    raise TypeError(f"Histogram requires numeric data: {series.name}")

  values = series.dropna().to_numpy(dtype=float)

  if len(values) == 0:
    return HistogramData(
      column=str(series.name),
      bin_edges=[],
      counts=[],
      percentages=[],
    )

  counts, bin_edges = np.histogram(
    values,
    bins=bins,
  )

  percentages = (
    counts / len(values) * 100
  )

  return HistogramData(
    column=str(series.name),
    bin_edges=bin_edges.tolist(),
    counts=counts.astype(int).tolist(),
    percentages=percentages.tolist(),
  )


def _dataset_histograms(df: pd.DataFrame) -> dict[str, HistogramData]:
  return {
    str(column): _dataset_histogram(df[column])
    for column in df.select_dtypes(include="number").columns
  }


# 7. CATEGORICAL DISTRIBUTION
def _categorical_distribution(
  series: pd.Series,
  top_n: int | None = None,
) -> CategoricalDistribution:
  counts = series.value_counts(dropna=False)

  if top_n is not None:
    counts = counts.head(top_n)

  total = len(series)

  frequencies = [
    CategoryFrequency(
      value=("<MISSING>" if pd.isna(value) else str(value)),
      count=int(count),
      percentage=(float(count / total * 100) if total else 0.0),
    )
    for value, count in counts.items()
  ]

  return CategoricalDistribution(
      column=str(series.name),
      unique=int(series.nunique(dropna=True)),
      frequencies=frequencies,
  )


def _dataset_categorical_distributions(
  df: pd.DataFrame,
  config: dict,
) -> dict[str, CategoricalDistribution]:
  results = {}

  columns_config = get_columns_config(config)

  for column, settings in columns_config.items():
    if column not in df.columns:
      continue

    semantic_type = settings.get("semantic_type")

    is_categorical = (
      semantic_type in {"nominal", "ordinal"}
      or pd.api.types.is_object_dtype(df[column])
      or isinstance(df[column].dtype, pd.CategoricalDtype)
      or pd.api.types.is_bool_dtype(df[column])
      or pd.api.types.is_string_dtype(df[column])
    )

    if is_categorical:
      results[column] = _categorical_distribution(df[column])

  return results


# 8. OUTLIER ANALYSIS
def _analyze_outliers(series: pd.Series) -> dict[str, Any]:
  if not pd.api.types.is_numeric_dtype(series):
    return {
      "column": str(series.name),
      "outlier_count": 0,
      "outlier_percentage": 0.0,
      "outlier_values": [],
    }

  values = series.dropna()

  if values.empty:
    return {
      "column": str(series.name),
      "outlier_count": 0,
      "outlier_percentage": 0.0,
      "outlier_values": [],
    }

  q1 = float(values.quantile(0.25))
  q3 = float(values.quantile(0.75))
  iqr = q3 - q1

  lower_bound = q1 - 1.5 * iqr
  upper_bound = q3 + 1.5 * iqr

  outliers = values[(values < lower_bound) | (values > upper_bound)]

  return {
    "column": str(series.name),
    "method": "IQR",
    "q1": q1,
    "q3": q3,
    "lower_bound": lower_bound,
    "upper_bound": upper_bound,
    "outlier_count": int(len(outliers)),
    "outlier_percentage": float(len(outliers) / len(values) * 100),
    "outlier_values": outliers.tolist(),
  }


def _dataset_outliers(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
  return {
    str(column): _analyze_outliers(df[column])
    for column in df.select_dtypes(include="number").columns
  }


# 9. CORRELATION ANALYSIS
def _dataset_correlations(df: pd.DataFrame) -> dict[str, Any]:
  numeric_df = df.select_dtypes(include="number")

  if numeric_df.shape[1] < 2:
      return {
        "columns": numeric_df.columns.tolist(),
        "matrix": {},
        "strong_correlations": [],
      }

  correlation = numeric_df.corr(method="pearson")

  strong_correlations = []

  columns = correlation.columns.tolist()

  for i, column_1 in enumerate(columns):
    for column_2 in columns[i + 1:]:
      value = correlation.loc[column_1, column_2]

      if pd.isna(value):
        continue

      if abs(value) >= 0.7:
        strong_correlations.append({
          "column_1": column_1,
          "column_2": column_2,
          "correlation": float(value),
        })

  return {
    "method": "pearson",
    "columns": columns,
    "matrix": correlation.to_dict(),
    "strong_correlations": strong_correlations,
  }


# 10. DATASET EDA PIPELINE
def analyze_dataset(df: pd.DataFrame, config: dict) -> DatasetProfiling:
  validate_columns(df, config)

  eda_config = config.get("eda", {})

  if not eda_config.get("enabled", True):
    return DatasetProfiling(
      dataset_name=config.get("name", ""),
      structure=_dataset_structure(df),
      quality=_dataset_quality(df, config)
    )

  checks = eda_config.get(
    "checks",
    [
      "descriptivestatistics",
      "distributions",
      "outliers",
      "correlations",
    ],
  )

  results = {}

  for check in checks:
    if check == "descriptivestatistics":
      distributions = _dataset_distribution(df)

    elif check == "distributions":
      results["histograms"] = (_dataset_histograms(df))
      results["categorical_distributions"] = (
        _categorical_distribution(df, config)
      )

    elif check == "outliers":
      results["outliers"] = _dataset_outliers(df)

    elif check == "correlations":
      results["correlations"] = (_dataset_correlations(df))

    else:
      raise ValueError(f"Unsupported EDA check: {check}")

  return DatasetProfiling(
    dataset_name=config.get("name", ""),
    structure=_dataset_structure(df),
    quality=_dataset_quality(df, config),

    distributions=_dataset_distribution(df),
    categorical_distributions=_categorical_distribution(df),
    histograms=_dataset_histograms(df),
    boxplots=_dataset_outliers(df)

  )

# 11. MAIN
if __name__ == "__main__":
  dataset_config, frame = load_dataset()

  print("Dataset information:")
  frame.info()

  result = analyze_dataset(frame, dataset_config)