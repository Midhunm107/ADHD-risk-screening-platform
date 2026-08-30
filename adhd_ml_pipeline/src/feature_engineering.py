"""
feature_engineering.py

Merges real HYPERAKTIV feature sources into one modeling table. All three
are genuinely measured data - no synthesis involved:
  1. Real questionnaire scores (ASRS/WURS/MADRS/HADS) from patient_info.csv
  2. Real CPT-II clinical summary scores (T-scores, raw scores, etc.)
  3. Real tsfresh actigraphy features (787 cols) - optional, known to
     underperform at this sample size per prior work; included as a
     separate ablation, not folded silently into the main feature set.

Base table is patient_info (103 patients) - this means the 31 extra IDs
in features.csv that fall outside patient_info's ID range are correctly
excluded, and the 18 patients without actigraphy data get NaN in those
columns rather than being dropped.
"""
from pathlib import Path

import pandas as pd

from src import data_loading


def build_feature_dataset(config: dict, include_actigraphy: bool = False) -> pd.DataFrame:
    id_col = config["columns"]["id_col"]
    label_col = config["columns"]["label_col"]
    adhd_value = config["columns"]["adhd_value"]

    patient_info = data_loading.load_patient_info(config)
    cpt = data_loading.load_cpt_summary_features(config)
    questionnaire = data_loading.load_questionnaire_features(config)

    label = (patient_info[label_col] == adhd_value).astype(int).rename("label")
    merged = pd.concat([patient_info[[id_col]], label], axis=1)

    merged = merged.merge(cpt, on=id_col, how="left")
    merged = merged.merge(questionnaire, on=id_col, how="left")

    if include_actigraphy:
        actigraphy = data_loading.load_actigraphy_features(config)
        if actigraphy is not None:
            merged = merged.merge(actigraphy, on=id_col, how="left", suffixes=("", "_actigraphy"))

    missing = merged.isna().sum()
    cols_with_missing = missing[missing > 0]
    if len(cols_with_missing):
        print(
            f"Note: {len(cols_with_missing)} columns have missing values "
            f"(expected - not every patient completed every assessment)."
        )

    out_path = Path(config["paths"]["feature_dataset"])
    if include_actigraphy:
        out_path = out_path.with_stem(out_path.stem + "_with_actigraphy")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out_path, index=False)
    print(
        f"Wrote feature dataset: {merged.shape[0]} rows, {merged.shape[1]} columns "
        f"(include_actigraphy={include_actigraphy}) -> {out_path}"
    )
    return merged


if __name__ == "__main__":
    cfg = data_loading.load_config()
    print("Building feature dataset WITHOUT actigraphy (CPT-II + questionnaire):")
    build_feature_dataset(cfg, include_actigraphy=False)
    print("\nBuilding feature dataset WITH actigraphy (known dimensionality risk):")
    build_feature_dataset(cfg, include_actigraphy=True)
