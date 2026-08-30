"""
eda.py

Basic exploratory analysis on the merged feature dataset: group summary
statistics (ADHD vs control) and a correlation heatmap, saved to
reports/figures/. Run after feature_engineering.py.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless - safe for scripts/CI, not just notebooks
import matplotlib.pyplot as plt
import pandas as pd

from src import data_loading


def summarize_by_label(df: pd.DataFrame, exclude_cols: list[str]) -> pd.DataFrame:
    numeric_cols = [
        c for c in df.select_dtypes(include="number").columns if c not in exclude_cols
    ]
    return df.groupby("label")[numeric_cols].agg(["mean", "std"]).T


def plot_correlation_heatmap(df: pd.DataFrame, exclude_cols: list[str], out_path: Path):
    numeric_cols = [
        c for c in df.select_dtypes(include="number").columns if c not in exclude_cols
    ]
    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(max(6, len(numeric_cols) * 0.5), max(5, len(numeric_cols) * 0.5)))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=90, fontsize=7)
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_yticklabels(numeric_cols, fontsize=7)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Feature correlation heatmap")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def run_eda(config: dict):
    df = pd.read_csv(config["paths"]["feature_dataset"])
    id_col = config["columns"]["id_col"]
    exclude_cols = [id_col, "label"]

    summary = summarize_by_label(df, exclude_cols)
    summary_path = Path("reports/eda_summary.csv")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(summary_path)
    print(f"Wrote group summary stats -> {summary_path}")

    heatmap_path = Path("reports/figures/correlation_heatmap.png")
    plot_correlation_heatmap(df, exclude_cols, heatmap_path)
    print(f"Wrote correlation heatmap -> {heatmap_path}")

    print(f"\nLabel balance:\n{df['label'].value_counts()}")


if __name__ == "__main__":
    cfg = data_loading.load_config()
    run_eda(cfg)
