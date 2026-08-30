"""
data_loading.py

Loads and validates the three real HYPERAKTIV files. All three are
semicolon-delimited (not comma) - confirmed directly from the uploaded files,
don't use pd.read_csv's default sep.

Real column names (confirmed from the actual files, not guessed):
  patient_info.csv: ID, SEX, AGE (coded 1-4, not raw years - likely
    quartile-binned for anonymization), ADHD (0/1 label), plus real
    clinical scores WURS/ASRS/MADRS/HADS_A/HADS_D, plus a CPT_II completion
    flag (0/1).
  CPT_II_ConnersContinuousPerformanceTest.csv: ID + 720 raw per-trial columns
    (Trial1/Response1..Trial360/Response360) + ~60 real summary/clinical
    columns (T-scores, raw scores, percentiles, confidence indices). Only
    99/103 patients have a row here - matches patient_info's CPT_II flag
    exactly.
  features.csv: ID + 787 already-computed tsfresh actigraphy (ACC) features.
    No extraction needed - this is a finished feature table, not raw signal.
"""
import sys
from pathlib import Path

import pandas as pd
import yaml

# Summary/clinical columns from the CPT-II export - everything that is NOT a
# raw per-trial Trial*/Response* column. These are the real T-scores/raw
# scores behind the established CPT-II + demographics baseline.
CPT_METADATA_COLS = ["Assessment Status", "Assessment Duration", "Type", "LastTrial"]


def load_config(config_path: str = "configs/config.yaml") -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def _read_semicolon_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        sys.exit(f"File not found: {path}")
    return pd.read_csv(path, sep=";")


def load_patient_info(config: dict) -> pd.DataFrame:
    df = _read_semicolon_csv(Path(config["paths"]["patient_info"]))
    id_col = config["columns"]["id_col"]
    label_col = config["columns"]["label_col"]
    if id_col not in df.columns or label_col not in df.columns:
        print(f"Columns found: {list(df.columns)}")
        sys.exit(f"id_col='{id_col}' or label_col='{label_col}' not found - fix configs/config.yaml")
    return df


def load_cpt_summary_features(config: dict) -> pd.DataFrame:
    """
    Loads only the real summary/clinical columns from the CPT-II export -
    the T-scores, raw scores, percentiles, and confidence indices - and
    drops the 720 raw per-trial Trial*/Response* columns, which are the raw
    trial log rather than the clinical summary features the 72.7% baseline
    was built on.

    Only 99/103 patients completed the CPT-II (see patient_info's CPT_II
    flag) - this returns 99 rows, and the merge in feature_engineering.py
    is a left join, so patients without CPT-II data will have NaN CPT
    features rather than being silently dropped.
    """
    path = Path(config["paths"]["cpt_raw"])
    df = _read_semicolon_csv(path)
    id_col = config["columns"]["id_col"]

    trial_cols = [c for c in df.columns if c.startswith("Trial") or c.startswith("Response")]
    summary_cols = [c for c in df.columns if c not in trial_cols and c != id_col]
    # Drop non-numeric metadata columns (Assessment Status/Type/etc) - keep
    # only numeric clinical scores as model features.
    numeric_summary_cols = [
        c for c in summary_cols if c not in CPT_METADATA_COLS
    ]

    out = df[[id_col] + numeric_summary_cols].copy()
    out = out.add_prefix("cpt_")
    out = out.rename(columns={f"cpt_{id_col}": id_col})
    return out


def load_actigraphy_features(config: dict) -> pd.DataFrame:
    """
    features.csv is already a finished tsfresh feature table (787 columns,
    ACC__ prefixed) - no extraction needed, just load and return it.

    NOTE: your prior work found these 787 features underperform badly at
    this sample size (severe dimensionality mismatch - more features than
    patients). Treat as experimental/optional in feature_engineering.py
    rather than assuming inclusion helps.
    """
    path = Path(config["paths"]["actigraphy_features"])
    if not path.exists():
        print(f"No actigraphy feature file at {path} - skipping.")
        return None
    return _read_semicolon_csv(path)


def load_questionnaire_features(config: dict) -> pd.DataFrame:
    """
    Real clinical questionnaire scores, pulled directly from patient_info.csv
    - ASRS, WURS, MADRS, HADS_A, HADS_D. These are measured, not synthetic;
    the earlier synthetic ASRS generator (src/asrs_synthesis.py) is not used
    for this dataset since real scores exist. See config.yaml's
    columns.questionnaire_cols docstring for the ASRS instrument caveat.
    """
    patient_info = load_patient_info(config)
    id_col = config["columns"]["id_col"]
    q_cols = config["columns"]["questionnaire_cols"]
    missing = [c for c in q_cols if c not in patient_info.columns]
    if missing:
        sys.exit(f"questionnaire_cols {missing} not found in patient_info.csv")
    return patient_info[[id_col] + q_cols].copy()


if __name__ == "__main__":
    cfg = load_config()
    pinfo = load_patient_info(cfg)
    print(f"patient_info: {pinfo.shape[0]} rows, {pinfo.shape[1]} columns")
    print(f"  label balance: {pinfo[cfg['columns']['label_col']].value_counts().to_dict()}")

    cpt = load_cpt_summary_features(cfg)
    print(f"\nCPT-II summary: {cpt.shape[0]} rows, {cpt.shape[1]} columns (99 expected, not 103 - not all patients completed it)")

    actig = load_actigraphy_features(cfg)
    if actig is not None:
        print(f"\nActigraphy features: {actig.shape[0]} rows, {actig.shape[1]} columns")

    q = load_questionnaire_features(cfg)
    print(f"\nQuestionnaire (real, not synthetic): {q.shape[0]} rows, {q.shape[1]} columns")
    print(q.describe())
