import fractions
from dataclasses import dataclass, field

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from mlproject.data.loader import DatasetBundle


@dataclass
class MissingValues:
  marker: dict
  numeric: str
  categorical: str
  drop_rows_if_target_missing: bool

@dataclass
class Duplicates:
  mode: str
  strategy_candidates: str
  keep: str
  subnet: str | None = None

@dataclass
class CleanValidation:
  check_infinite_values: bool
  check_constant_features: bool
  check_duplicate_columns: bool

@dataclass
class CleanConfig:
  missing_values: MissingValues
  duplicates: Duplicates
  validation: CleanValidation

@dataclass
class SplitDefinition:
  splitter: dict
  shuffle: bool
  n_splits: int | None = None
  test_size: float | None = None
  random_state: int| None = None

  def validate(self):
    if 0 <= self.test_size <= 1:
      raise AttributeError(f"Split test size should in range 0 and 1")

@dataclass
class SplitConfig:
  strategy: str
  cv: bool
  splitter: list[SplitDefinition] \
    = field(default_factory=list[SplitDefinition])

@dataclass
class TransformConfig:
  scaler_candidates: str
  numeric_imputer_candidates: str
  categorical_imputer_candidates: str
  encoder_candidates: str
  feature_selection: bool
  selection_strategy: str
  threshold: float = 0.0

@dataclass(frozen=True)
class DataSplit:
  train_indices: np.ndarray
  test_indices: np.ndarray
  groups: pd.Series | None = None

def predictor_group_ids(
    frame: pd.DataFrame, feature_columns: tuple[str]
) -> pd.Series:

  missing = set(feature_columns).difference(frame.columns)
  if missing:
      raise ValueError(f"Cannot form duplicate groups; missing columns: {sorted(missing)}")
  group_index = pd.MultiIndex.from_frame(frame.loc[:, feature_columns])
  codes, _ = pd.factorize(group_index, sort=False)
  return pd.Series(codes, index=frame.index, name="duplicate_group")

def make_holdout_split(
    dataset_bundle: DatasetBundle
) -> DataSplit:
  frame = dataset_bundle.get("dataframe")
  feature_columns = dataset_bundle.get("features")
  target = dataset_bundle.get("target")
  groups = predictor_group_ids(frame, feature_columns)

  splitter = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
  )

  train_indices, test_indices = next(
    splitter.split(frame.loc[:, feature_columns], frame[target], groups)
  )

  train_groups = set(groups.iloc[train_indices])
  test_groups = set(groups.iloc[test_indices])
  if train_groups.intersection(test_groups):
    raise RuntimeError("Duplicate groups crossed the final hold-out boundary")

  return DataSplit(train_indices, test_indices, groups)

def split_xy(
    dataset_bundle: DatasetBundle, split: DataSplit, feature_columns: tuple[str, ...]
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
  frame, target, features = set(dataset_bundle)
  if target in feature_columns:
    raise ValueError("Target must not appear in predictor columns")
  train = frame.iloc[split.train_indices]
  test = frame.iloc[split.test_indices]
  return (
    train.loc[:, feature_columns].copy(),
    test.loc[:, feature_columns].copy(),
    train[target].copy(),
    test[target].copy(),
    split.groups.iloc[split.train_indices].copy(),
  )