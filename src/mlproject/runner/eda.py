from dataclasses import dataclass
from typing import Any, Literal, Union

import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

@dataclass(frozen=True)
class NumericalStatistics:
  mean: float| None
  median: float| None
  std: float| None
  min: float| None
  max: float| None
  q1: float| None
  q3: float| None
  iqr: float| None
  skewness: float| None
  kurtosis: float| None
  outlier_count: int

@dataclass(frozen=True)
class CategoricalStatistics:
  unique_count: int
  mode: str
  mode_count: int
  mode_percentage: float
  top_categories: list[Any]
  rare_categories: list[Any]


FEATURE_STATISTICS_DETAIL = Union[NumericalStatistics | CategoricalStatistics]
FEATURE_TYPE = Literal["numerical", "categorical"]

@dataclass
class FeatureStatistics:
  feature_name: str
  total_count: int
  valid_count: int
  missing_count: int
  missing_percentage: float
  unique_count: int
  datatype: FEATURE_TYPE
  statistics: FEATURE_STATISTICS_DETAIL

def eda_section(frame: pd.DataFrame, columns: dict[str, dict[str, Any]]) -> None:
  histogram_chart(frame, columns)
  return

def histogram_chart(frame: pd.DataFrame, columns: dict[str, dict[str, Any]]) -> None:
  for col, value in columns.items():
    sns.histplot(
      data=frame,
      x=col,
      bins=30,
      kde=True,
      color="skyblue",
      edgecolor="black"
    )

    plt.xscale("log")

    plt.title("Distribute of " + col, fontsize=14)
    plt.xlabel(col)
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()
  return