from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class OutputContext:
  dataset_id: str
  experiment_name: str
  run_id: str | None = None

@dataclass(frozen=True)
class OutputConfig:
  root_dir: Path = Path("outputs")
  overwrite: bool = False

