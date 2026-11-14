from dataclasses import dataclass, field

import pandas as pd
import numpy as np

@dataclass
class MissingStrategy:
  numeric: str | None = None
  categorical: str | None = None

@dataclass
class MissingConfig:
  markers: dict = field(default_factory=dict)
  drop_rows_if_target_missing: bool = True

@dataclass
class DuplicatesConfig:
  mode: str
  strategy_candidates: str
  subnet: str | None = None
  per_model: bool = True

@dataclass
class CleanInfo:
  missing_config: MissingConfig
  duplicates_config: DuplicatesConfig

@dataclass
class CVSplit:
  n_splits: int
  spliter: None = None

class HoldOutSplit:
  test_size: float
  spliter: None = None

@dataclass
class SplitInfor:
  random_state: int
  shuffle: bool
  split: CVSplit | HoldOutSplit

@dataclass
class TransformerConfig:
  name: str
  transformer: dict
