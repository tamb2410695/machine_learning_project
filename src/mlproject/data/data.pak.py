
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from mlproject.config import (
  DATA_PATH,
  TARGET,
  EXPECTED_COLUMNS,
  NUMERIC_FEATURES,
  CATEGORICAL_FEATURES,
  KEEP_DUPLICATE, DROP_DUPLICATE
)

@dataclass(frozen=True)
class DataSplit:
  train_indices: np.ndarray
  test_indices: np.ndarray
  groups: pd.Series

def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
  """Load the repository CSV and validate its schema and basic invariants."""

  if not path.is_file():
    raise FileNotFoundError(f"Dataset not found: {path}")
  frame = pd.read_csv(path)

  if set(frame.columns) != set(EXPECTED_COLUMNS):
    raise ValueError(
      "Unexpected dataset schema. "
      f"Expected {list(EXPECTED_COLUMNS)}, got {frame.columns.tolist()}"
    )
  if frame.empty:
    raise ValueError("Dataset is empty")

  if frame.isna().any().any():
    missing = frame.isna().sum()
    raise ValueError(f"Dataset contains missing values: {missing[missing > 0].to_dict()}")

  for column in NUMERIC_FEATURES:
      frame[column] = pd.to_numeric(frame[column], errors="raise")
  for column in CATEGORICAL_FEATURES:
    if not pd.api.types.is_object_dtype(frame[column]):
      pass

  return frame

def _drop_duplicate(frame: pd.DataFrame, strategy: str=KEEP_DUPLICATE) -> pd.DataFrame:
  if strategy == DROP_DUPLICATE:
    frame.drop_duplicates()
  return frame

# def _split_train_test()

if __name__ == "__main__":
  df = load_dataset()
  print(df.shape)
  print(len(df))
  print(len(df.columns))
  print(df.columns.tolist())
  print(df.dtypes)
  print(df.isna().sum())

  print(f"Duplicate rows: {df.duplicated().sum():,}")
  print(f"Duplicate rate: {df.duplicated().mean():.2%}")
  print(df.nunique())
  print(df.describe())
  print(df.head(10))
  print("\n=== FEATURE SUMMARY ===")

  summary = pd.DataFrame({
    "dtype": df.dtypes.astype(str),
    "missing": df.isna().sum(),
    "missing_rate": df.isna().mean(),
    "unique": df.nunique(),
  })

  print(df["amneties"].value_counts().sort_index())
  print(df["status"].value_counts().sort_index())
  print(df["age"].value_counts().sort_index())

  print(summary)
