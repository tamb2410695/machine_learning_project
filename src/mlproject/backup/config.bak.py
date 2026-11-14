from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "dataset" / "data.csv"
EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"
COMPARISONS_DIR = PROJECT_ROOT / "comparisons"

# Experiment settings
TARGET = "price"
RANDOM_STATE = 42

# Experiment options
KEEP_DUPLICATE = "keep"
DROP_DUPLICATE = "drop"
DUPLICATE_OPTIONS = (
  KEEP_DUPLICATE,
  DROP_DUPLICATE
)

HOLDOUT_SPLITS = "hold_out"
KFOLD_SPLITS = "k_fold"
SPLIT_OPTIONS = {
  HOLDOUT_SPLITS: [5],
  KFOLD_SPLITS: [5]
}

# Feature groups
NUMERIC_FEATURES = (
    "age",
    "amneties",
    "area",
    "atmDistance",
    "balconies",
    "bathrooms",
    "hospitalDistance",
    "restrauntDistance",
    "schoolDistance",
    "shoppingDistance",
)

CATEGORICAL_FEATURES = (
    "status",
)

# Dataset schema
FEATURE_COLUMNS = (*NUMERIC_FEATURES, *CATEGORICAL_FEATURES,)

# Experiment variants
EXPECTED_COLUMNS = (*FEATURE_COLUMNS, TARGET)

EXPERIMENT_FEATURE = {
  "Full": FEATURE_COLUMNS
}

EXPERIMENT_DESCRIPTIONS = {
    "Full": "All valid predictors, including Height and Weight."
}

# Encoding groups
BINARY_CATEGORICAL = ()

NOMINAL_CATEGORICAL = (
    "status",
)

ORDINAL_LIKE_CATEGORICAL = ()

# Numeric transformation groups
CONTINUOUS_NUMERIC = (
    "area",
    "atmDistance",
    "hospitalDistance",
    "restrauntDistance",
    "schoolDistance",
)

INTERPOLATED_SCALE_NUMERIC = (
    "age",
    "amneties",
    "balconies",
    "bathrooms",
)

# Output initialization
def ensure_output_directories() -> None:
  for path in (EXPERIMENTS_DIR, COMPARISONS_DIR):
    path.mkdir(parents=True, exist_ok=True)