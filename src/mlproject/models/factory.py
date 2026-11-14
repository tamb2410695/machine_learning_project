"""
WE NEED @DATACLASS
This file should save @dataclass for models
and some helper function for these @dataclass

Not running model at here
"""

from dataclasses import dataclass

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import (
  GridSearchCV,
  StratifiedGroupKFold,
  train_test_split,
  GroupShuffleSplit
)
from sklearn.pipeline import Pipeline

from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB

from mlproject.config import load_model_config


@dataclass(frozen=True)
class ModelDefinition:
  name: str
  id: str
  task: str
  estimator: BaseEstimator
  parameter_grid: dict[str, list[object]]
  scale_numeric: bool = False
  rationale: str = ""

@dataclass
class SearchOutcome:
  experiment: str
  model: str
  task: str
  search: GridSearchCV
  fit_seconds: float
  rationale: str

def load_model_definition(model_config: dict) -> tuple[ModelDefinition, ...]:
  return tuple(
    ModelDefinition(
      name=model["label"],
      id=model["id"],
      task=model["task"],
      estimator=model["estimator"],
      parameter_grid=model["parameter_grid"],
      scale_numeric=model.get("scale_numeric", False),
    )
    for model in model_config.values()
    if model.get("enable", False),
  )

def _pipeline(experiment: str, definition: ModelDefinition) -> Pipeline:
  return Pipeline(
    [
      ("preprocess", ),
      ("model", definition.estimator)
    ]
  )

def fit_model_searches(
    experiment: str,
    x_train: pd.DataFrame,
    y_train: pd.DataFrame,
    train_groups: pd.Series
) -> list[SearchOutcome]:
  cv = StratifiedGroupKFold()
  outcomes: list[SearchOutcome] = []

  return outcomes

if __name__ == "__main__":
  config = load_model_config()
  print(load_model_definition(config))