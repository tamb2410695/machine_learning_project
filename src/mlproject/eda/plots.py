import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
import seaborn as sns

from mlproject.data import load_dataset


def plot_missing_value(df: pd.DataFrame) -> Figure:
  missing = (
    df.isna()
    .sum()
    .sort_values(ascending=False)
  )
  missing = missing[missing > 0]

  fig, ax = plt.subplots(figsize=(10, 5))

  if missing.empty:
    ax.text(
      0.5, 0.5,
      "No missing values",
      ha="center",
      va="center",
    )
    ax.set_axis_off()
  else:
    sns.barplot(
      x=missing.values,
      y=missing.index,
      ax=ax,
    )
    ax.set_xlabel("Missing values")
    ax.set_ylabel("Column")
    ax.set_title("Missing Values by Column")

  fig.tight_layout()
  return fig

def plot_numeric_distribution(df: pd.DataFrame) -> Figure | None:
  return

def plot_categorical_distribution(df: pd.DataFrame) -> Figure | None:
  return

def plot_boxplots(df: pd.DataFrame) -> Figure | None:
  return

def plot_correlation_heatmap(df: pd.DataFrame) -> Figure | None:
  return

if __name__ == "__main__":
  _, df = load_dataset()
  fig = plot_missing_value(df)
  fig.show()