"""
train.py

Trains Logistic Regression, Random Forest, and XGBoost with stratified k-fold
CV (matches your existing HYPERAKTIV baseline methodology) across three real
feature-set variants:

  1. cpt_only            - CPT-II clinical summary only (replicates your
                            established 72.7% baseline as a sanity check)
  2. cpt_questionnaire    - CPT-II + real ASRS/WURS/MADRS/HADS scores (the
                            "Standardized Questionnaire" branch from your
                            diagram, using real measured data)
  3. cpt_questionnaire_actigraphy - adds the 787 tsfresh actigraphy features
                            (known dimensionality risk per your prior work -
                            report this one with that caveat attached)

All three use real data - no synthetic features anywhere in this file.
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

from src import data_loading

try:
    from xgboost import XGBClassifier

    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False


MODEL_BUILDERS = {
    "logistic_regression": lambda seed: LogisticRegression(max_iter=1000, random_state=seed),
    "random_forest": lambda seed: RandomForestClassifier(n_estimators=200, random_state=seed),
}
if HAS_XGBOOST:
    MODEL_BUILDERS["xgboost"] = lambda seed: XGBClassifier(
        eval_metric="logloss", random_state=seed
    )

QUESTIONNAIRE_COLS = ["ASRS", "WURS", "MADRS", "HADS_A", "HADS_D"]


def load_feature_matrix(
    config: dict, feature_group: str
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    feature_group: "cpt_only" | "cpt_questionnaire" | "cpt_questionnaire_actigraphy"
    """
    id_col = config["columns"]["id_col"]
    use_actigraphy = feature_group == "cpt_questionnaire_actigraphy"
    dataset_path = Path(config["paths"]["feature_dataset"])
    if use_actigraphy:
        dataset_path = dataset_path.with_stem(dataset_path.stem + "_with_actigraphy")

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"{dataset_path} not found - run `python -m src.feature_engineering` first."
        )
    df = pd.read_csv(dataset_path)

    numeric_cols = [c for c in df.select_dtypes(include="number").columns if c not in (id_col, "label")]
    cpt_cols = [c for c in numeric_cols if c.startswith("cpt_")]

    if feature_group == "cpt_only":
        feature_cols = cpt_cols
    elif feature_group == "cpt_questionnaire":
        feature_cols = cpt_cols + [c for c in QUESTIONNAIRE_COLS if c in numeric_cols]
    elif feature_group == "cpt_questionnaire_actigraphy":
        feature_cols = numeric_cols  # everything, including ACC__ actigraphy columns
    else:
        raise ValueError(f"Unknown feature_group: {feature_group}")

    X_df = df[feature_cols]
    # Drop columns that are 100% NaN (median is undefined) - a handful of
    # tsfresh features (e.g. friedrich_coefficients, max_langevin_fixed_point)
    # fail to compute for every subject in this dataset and carry no signal.
    all_nan_cols = [c for c in X_df.columns if X_df[c].isna().all()]
    if all_nan_cols:
        print(f"Dropping {len(all_nan_cols)} all-NaN columns: {all_nan_cols}")
        X_df = X_df.drop(columns=all_nan_cols)
        feature_cols = [c for c in feature_cols if c not in all_nan_cols]

    X = X_df.fillna(X_df.median()).to_numpy()
    y = df["label"].to_numpy()
    return X, y, feature_cols


def cross_validate_model(model_name: str, X: np.ndarray, y: np.ndarray, config: dict) -> dict:
    cv_folds = config["training"]["cv_folds"]
    seed = config["training"]["random_seed"]
    skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=seed)

    accuracies, sensitivities, specificities = [], [], []
    for train_idx, val_idx in skf.split(X, y):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)

        model = MODEL_BUILDERS[model_name](seed)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)

        tp = ((preds == 1) & (y_val == 1)).sum()
        fn = ((preds == 0) & (y_val == 1)).sum()
        tn = ((preds == 0) & (y_val == 0)).sum()
        fp = ((preds == 1) & (y_val == 0)).sum()

        accuracies.append((preds == y_val).mean())
        sensitivities.append(tp / (tp + fn) if (tp + fn) > 0 else np.nan)
        specificities.append(tn / (tn + fp) if (tn + fp) > 0 else np.nan)

    return {
        "model": model_name,
        "accuracy_mean": np.mean(accuracies),
        "accuracy_std": np.std(accuracies),
        "sensitivity_mean": np.nanmean(sensitivities),
        "specificity_mean": np.nanmean(specificities),
    }


def run_training(config: dict, feature_group: str, save_best: bool = False) -> pd.DataFrame:
    X, y, feature_cols = load_feature_matrix(config, feature_group)
    print(f"Training on {X.shape[0]} samples, {X.shape[1]} features (feature_group={feature_group})")

    models_to_run = [m for m in config["training"]["models"] if m in MODEL_BUILDERS]
    missing = set(config["training"]["models"]) - set(models_to_run)
    if missing:
        print(f"Skipping unavailable models (not installed?): {missing}")

    results = [cross_validate_model(m, X, y, config) for m in models_to_run]
    results_df = pd.DataFrame(results).sort_values("accuracy_mean", ascending=False)

    report_path = Path(config["paths"]["model_comparison_report"]).with_stem(
        Path(config["paths"]["model_comparison_report"]).stem + f"_{feature_group}"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(report_path, index=False)
    print(f"\nResults ({feature_group}):")
    print(results_df.to_string(index=False))
    print(f"Wrote comparison report -> {report_path}")

    if save_best:
        best_model_name = results_df.iloc[0]["model"]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        best_model = MODEL_BUILDERS[best_model_name](config["training"]["random_seed"])
        best_model.fit(X_scaled, y)
        model_path = Path(config["paths"]["best_model"])
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": best_model, "scaler": scaler, "feature_cols": feature_cols}, model_path)
        print(f"Saved best model ({best_model_name}) -> {model_path}")

    return results_df


if __name__ == "__main__":
    cfg = data_loading.load_config()

    print("=" * 70)
    print("RUN 1: cpt_only (replicates your established 72.7% baseline)")
    print("=" * 70)
    run_training(cfg, "cpt_only")

    print("\n" + "=" * 70)
    print("RUN 2: cpt_questionnaire (CPT-II + real ASRS/WURS/MADRS/HADS)")
    print("=" * 70)
    run_training(cfg, "cpt_questionnaire", save_best=True)

    print("\n" + "=" * 70)
    print("RUN 3: cpt_questionnaire_actigraphy (adds 787 tsfresh features - dimensionality risk)")
    print("=" * 70)
    run_training(cfg, "cpt_questionnaire_actigraphy")
