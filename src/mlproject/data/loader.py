"""
Load dataset, config, and validate some simple condition
I think config should save experiment config like target, feature.
But dataset.yaml should config simple attribute like path, columns, label, eda settings, etc.

and... load experiment.yaml?
"""
from dataclasses import dataclass
from typing import Any

import pandas as pd

from mlproject.config import load_dataset_config


@dataclass
class DatasetBundle:
  key: str
  name: str
  frame: pd.DataFrame
  columns: dict[str, dict[str, Any]]
  target: str
  features: list[dict[str, Any]]


def load_dataset(dataset_key: str) -> DatasetBundle:
  dataset_config, dataset_dir = load_dataset_config(dataset_key)
  if not dataset_dir.exists():
    raise FileNotFoundError(f"Not found dataset file: {dataset_dir}")
  dataset_name = dataset_config.get("name")

  if dataset_dir.suffix.lower() == ".csv":
    return DatasetBundle(
      key=dataset_key,
      name=dataset_name,
      frame=pd.read_csv(dataset_dir),
      columns=get_columns_config(dataset_config),
      target=get_target(dataset_config),
      features=get_features(dataset_config)
    )

  if dataset_dir.suffix.lower() in [".xlsx", ".xls"]:
    return DatasetBundle(
      key=dataset_key,
      name=dataset_name,
      frame=pd.read_excel(dataset_dir),
      columns=get_columns_config(dataset_config),
      target=get_target(dataset_config),
      features=get_features(dataset_config)
    )

  raise ValueError("Only support CSV and Excel")

def get_columns_config(config: dict) -> dict[str, dict]:
  columns = config.get("columns", {})
  if not isinstance(columns, dict):
    raise ValueError(
      "'columns' must be a mapping of column names to settings"
    )
  return columns


def get_target(config: dict) -> str:
  columns_config = get_columns_config(config)
  targets = [
    name
    for name, settings in columns_config.items()
    if settings.get("role") == "target"
  ]
  if len(targets) != 1:
    raise ValueError(
      f"Expected exactly one target column, found: {targets}"
    )
  return targets[0]

def get_features(config: dict) -> list:
  columns_config = get_columns_config(config)
  features = [
    name
    for name, settings in columns_config.items()
    if settings.get("role") == "feature"
  ]
  if len(features) == 0:
    raise ValueError(
      f"Expected features at leats one column, found: {features}"
    )
  return features

def get_numeric_features(config: dict) -> dict[str, Any]:
  columns_config = get_columns_config(config)
  numeric_features = {
    str(settings.get("semantic_type")): name
      for name, settings in columns_config.items()
      if settings.get("role") == "feature"
         and settings.get("expected_dtype") == "numeric"
  }
  return numeric_features


def validate_columns(df: pd.DataFrame, config: dict) -> None:
  columns_config = get_columns_config(config)
  missing_columns = [
    name
    for name in columns_config
    if name not in df.columns
  ]

  if missing_columns:
    raise ValueError(
      f"Configured columns missing from dataset: "
      f"{missing_columns}"
    )
