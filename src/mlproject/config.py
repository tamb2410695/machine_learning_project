from pathlib import Path
from typing import Any

import yaml

# Directories
PACKAGE_DIR = Path(__file__).resolve().parent
ROOT_DIR = (PACKAGE_DIR / "../..").resolve()
CONFIG_DIR = ROOT_DIR / "config"


# Config files
CONFIG_FILE = PACKAGE_DIR / "default.yaml"

DATASET_CONFIG_FILE = CONFIG_DIR / "dataset.yaml"
PREPARE_CONFIG_FILE = CONFIG_DIR / "preprocessing.yaml"
MODEL_CONFIG_FILE = CONFIG_DIR / "model.yaml"
ARTIFACT_CONFIG_FILE = CONFIG_DIR / "artifact.yaml"
EXPERIMENT_CONFIG_FILE = CONFIG_DIR / "experiment.yaml"

# Selected dataset
DATASET_NAME = "kerala_house_price"


def read_yaml(path: Path) -> dict:
  with path.open("r", encoding="utf-8") as file:
    return yaml.safe_load(file) or {}

def load_app_config() -> dict:
  return read_yaml(CONFIG_FILE)

def get_root_dir() -> Path:
  return ROOT_DIR

def get_profiling_dir() -> Path:
  app_config = load_app_config()
  profiling_dir = (
      ROOT_DIR / app_config["directory"]["profiling"]
  ).resolve()
  return profiling_dir

def get_experiments_dir() -> Path:
  app_config = load_app_config()
  experiments_dir = (
      ROOT_DIR / app_config["directory"]["experiments"]
  ).resolve()
  return experiments_dir

def get_comparisons_dir() -> Path:
  app_config = load_app_config()
  comparisons_dir = (
      ROOT_DIR / app_config["directory"]["comparisons"]
  ).resolve()
  return comparisons_dir

def load_config(config_file: Path) -> dict:
  return read_yaml(config_file)

def load_dataset_config(dataset_name: str) -> tuple[dict, Path]:
  configs = load_config(DATASET_CONFIG_FILE)
  if DATASET_NAME not in configs:
    raise KeyError(
      f"Dataset '{dataset_name}' not found in "
      f"{DATASET_CONFIG_FILE}"
    )

  dataset_config = configs[dataset_name]
  dataset_path = (
        get_root_dir() / dataset_config["directory"]
    ).resolve()

  if not dataset_path.is_file():
    raise FileNotFoundError(
      f"Dataset file not found: {dataset_path}"
    )
  return dataset_config, dataset_path

def load_preprocessing_config() -> dict:
  return load_config(PREPARE_CONFIG_FILE)

def load_models_config() -> dict:
  return load_config(MODEL_CONFIG_FILE)

def load_artifact_config() -> dict:
  return load_config(ARTIFACT_CONFIG_FILE)

def load_experiment_config() -> dict:
  return load_config(EXPERIMENT_CONFIG_FILE)

def get_experiment_config(experiment_name: str, experiment_config: dict[str, Any]) \
    -> tuple[list[Any], ...]:
  config: dict[str, Any] = experiment_config.get(experiment_name, "")
  dataset_key = config.get("dataset_key")
  task = config.get("task")
  dataset_target = config.get("target")
  dataset_features = config.get("features")

  preprocessing_config = config.get("preprocessing")
  clean_config = preprocessing_config.get("clean")
  split_config = preprocessing_config.get("split")
  transform_config = preprocessing_config.get("transform")

  models_config = config.get("model")
  runs_config = config.get("runs")
  return (
    [
      dataset_key,
      task,
      dataset_target,
      dataset_features
    ],
    [
      clean_config,
      split_config,
      transform_config
    ],
    [
      models_config
    ],
    [
      runs_config
    ]
  )

def get_default_config() -> tuple:
  preprocessing_config = load_preprocessing_config()
  models_config = load_models_config()
  clean_config = preprocessing_config.get("clean")
  split_config = preprocessing_config.get("split")
  transform_config = preprocessing_config.get("transform")

  return (
    [
      clean_config,
      split_config,
      transform_config
    ],
    [
      models_config
    ],
  )
