from dataclasses import dataclass, field
from typing import Any, Literal

# 1. DATASET STRUCTURE
@dataclass
class ColumnSchema:
  name: str
  dtype: str
  role: str | None = None
  semantic_type: str | None = None
  nullable: bool | None = None


@dataclass
class DatasetStructure:
  n_rows: int
  n_columns: int
  columns: list[ColumnSchema] = field(default_factory=list)
  memory_mb: float = 0.0


# 2. DATA QUALITY
@dataclass
class MissingValueInfo:
  column: str
  missing_count: int
  missing_percentage: float

@dataclass
class DataQuality:
  duplicate_rows: int = 0
  duplicate_percentage: float = 0.0
  missing_values: list[MissingValueInfo] = field(
    default_factory=list
  )
  constant_columns: list[str] = field(default_factory=list)
  constraint_violations: dict[str, dict[str, int]] = field(
    default_factory=dict
  )


# 3. DESCRIPTIVE STATISTICS
@dataclass
class DistributionStats:
  count: int
  unique: int

  min: float | None = None
  max: float | None = None
  mean: float | None = None
  median: float | None = None
  std: float | None = None

  q1: float | None = None
  q3: float | None = None

  skewness: float | None = None
  kurtosis: float | None = None


@dataclass
class ColumnDistribution:
  name: str
  dtype: str
  semantic_type: str | None = None
  stats: DistributionStats | None = None


# 4. HISTOGRAM DATA
@dataclass
class HistogramData:
  column: str
  bin_edges: list[float] = field(default_factory=list)
  counts: list[int] = field(default_factory=list)
  percentages: list[float] = field(default_factory=list)


# 5. CATEGORICAL FREQUENCIES
@dataclass
class CategoryFrequency:
  value: str
  count: int
  percentage: float

@dataclass
class CategoricalDistribution:
  column: str
  unique: int
  frequencies: list[CategoryFrequency] = field(
      default_factory=list
  )


# 6. BOXPLOT AND OUTLIERS
@dataclass
class BoxPlotData:
  column: str

  min_value: float | None = None
  q1: float | None = None
  median: float | None = None
  q3: float | None = None
  max_value: float | None = None

  lower_bound: float | None = None
  upper_bound: float | None = None

  outliers: list[float] = field(default_factory=list)
  outlier_count: int = 0
  outlier_percentage: float = 0.0


# 7. CORRELATION MATRIX
@dataclass
class CorrelationPair:
  column_1: str
  column_2: str
  correlation: float

@dataclass
class CorrelationAnalysis:
  method: str = "pearson"
  columns: list[str] = field(default_factory=list)

  matrix: list[list[float | None]] = field(
    default_factory=list
  )

  strong_correlations: list[CorrelationPair] = field(
    default_factory=list
  )


# 8. SCATTER PLOT DATA
@dataclass
class ScatterPlotData:
  x_column: str
  y_column: str
  x_values: list[float] = field(default_factory=list)
  y_values: list[float] = field(default_factory=list)


# 9. CHART SPECIFICATION
@dataclass
class ChartSpec:
  chart_type: Literal[
    "histogram",
    "bar",
    "box",
    "scatter",
    "heatmap",
    "line",
  ]

  title: str
  x_label: str
  y_label: str

  data_key: str
  options: dict[str, Any] = field(default_factory=dict)

# 10. DATASET PROFILING
@dataclass
class DatasetProfiling:
  dataset_name: str

  structure: DatasetStructure
  quality: DataQuality

  distributions: dict[str, ColumnDistribution] = field(
    default_factory=dict
  )

  categorical_distributions: dict[
    str, CategoricalDistribution
  ] = field(default_factory=dict)

  histograms: dict[str, HistogramData] = field(
    default_factory=dict
  )

  boxplots: dict[str, BoxPlotData] = field(
    default_factory=dict
  )

  correlations: CorrelationAnalysis | None = None

  scatter_plots: dict[str, ScatterPlotData] = field(
    default_factory=dict
  )

  charts: list[ChartSpec] = field(default_factory=list)
