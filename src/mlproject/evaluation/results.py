"""
WE NEED @DATACLASS

I just forgot this module, it seems like eda module
It is final module of project flow
after that is export, pipeline, runner, cli, main, etc.
"""

from dataclasses import dataclass, field

@dataclass
class RegressionMetrics:
  accuracy: float
  mse: float
  rmse: float
  r2: float


@dataclass
class ClassificationMetrics:
  accuracy: float
  macro_precision: float


@dataclass
class EvaluationReportFrame:
  name: str
  experiment: str
  task: str
  result: RegressionMetrics | ClassificationMetrics | dict \
    = field(default_factory=dict)

