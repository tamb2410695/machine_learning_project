"""
WE NEED @DATACLASS - in the other file in this module


This file is for preprocessing running function
It will return data and preprocess config after running

So we need others file to set up @dataclass
"""
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from mlproject.config import load_experiment_config

def load_experiment(dataset_name: str) -> dict:
  try:
    experiment_config = load_experiment_config()
  except KeyError as exc:
    raise ValueError(f"Unknown dataset: {dataset_name}") from exc

  return experiment_config

def feature_types(dataset_name: str, experiment: str) -> tuple[list[str], list[str]]:
  try:
    experiment_config = load_experiment(dataset_name)
    selected = set(experiment_config[experiment])
  except KeyError as exc:
    raise ValueError(f"Unknown experiment: {experiment}") from exc

  numeric = []
  categorical = []
  return numeric, categorical

def build_preprocessor(dataset_name: str, experiment: str, config: dict) -> ColumnTransformer:
  numeric, categorical = feature_types(dataset_name, experiment)
  options: dict = config
  numeric_steps = list[tuple[str, object]]
  categorical_steps = list[tuple[str, object]]
  return ColumnTransformer(
    transformers=[
      ("numeric", Pipeline, numeric),
      (
        "categorical",
        Pipeline,
        categorical
      )
    ],
    remainder="drop",
    verbose_feature_names_out=True
  )