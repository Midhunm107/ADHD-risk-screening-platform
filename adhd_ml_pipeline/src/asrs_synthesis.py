"""
generate_synthetic_asrs.py

============================== READ THIS FIRST ==============================
HYPERAKTIV does not contain ASRS or any other questionnaire data - only
demographics, CPT-II scores, and actigraphy/heart-rate data. This script
GENERATES SYNTHETIC ASRS-v1.1 Part A responses, calibrated to each patient's
real diagnosis label (ADHD vs clinical control) using published screener
performance statistics as a target, NOT real patient self-report.

Every row this script outputs is synthetic. Every output file is prefixed
"synthetic_" and stamped with a data_source column. Do not merge this into a
"real" dataset without that label, and do not present model results that
depend on this file as if they were trained on genuine patient questionnaire
responses. In your report/methodology chapter, this needs its own explicit
paragraph: what was generated, why, using what calibration targets, and what
that means for how the results should be interpreted (i.e. this demonstrates
the *pipeline and methodology* for combining a questionnaire feature with
CPT-II/demographic features - it does not demonstrate that this particular
model would perform this way on genuine ASRS responses).
===============================================================================

Calibration targets (documented, not invented):
- HYPERAKTIV's "clinical controls" are patients referred for evaluation of
  ADHD/mood/anxiety disorders, not a general-population sample. The ASRS's
  headline sensitivity/specificity (68.7% / 99.5%; Kessler et al., 2005) was
  measured in a *general community* sample and does not transfer to a
  psychiatric clinical population - specificity in comorbid/clinical
  populations is reported far lower elsewhere in the literature (e.g. ~70%
  specificity in a treatment-seeking alcohol-use-disorder sample; ~71%
  specificity in a primary-care sample). This script therefore targets a
  more conservative, clinically-plausible calibration:
    ADHD group      -> ~80% screen positive (target "sensitivity")
    Control group   -> ~30% screen positive (i.e. ~70% "specificity")
  These are researcher-chosen targets for a *plausible clinical-population*
  calibration, not measured values - state this plainly in your report.

Method:
  Each patient gets a latent "symptom severity" value in [0,1] drawn from a
  Beta distribution whose mean differs by diagnosis group. Each of the 6
  ASRS Part A items is then sampled around that latent severity (with
  per-item noise, since real patients don't endorse every item identically)
  and discretized into the 0-4 Never..Very Often scale. The per-item
  scoring thresholds match the official ASRS-v1.1 shaded-box key.

Covariate adjustments (optional, off unless configured):
- AGE -> hyperactivity items only (q5 "fidget/squirm", q6 "driven by a
  motor"). Well-supported in the literature: hyperactive-impulsive symptoms
  decline with age in adults with ADHD while inattentive symptoms persist
  (Biederman, Mick & Faraone, 2000, Am J Psychiatry; consistently replicated,
  e.g. Kooij et al. review; NIMH/clinical overviews). Older age -> lower
  severity contribution to q5/q6 specifically, nothing else.
- SEX -> deliberately NOT applied by default. The evidence here is mixed:
  at least one case-control study using objective movement tracking found
  males and females with ADHD were equally hyperactive (Hjelmervik et al.,
  cited in the hyperactivity-persistence literature), which argues against
  baking in a sex effect on self-report hyperactivity items without better
  support. The knob exists (sex_hyperactivity_effect in config) if your guide
  specifically wants it modeled, but it defaults to 0 for both sexes.
- A generic continuous severity/symptom-burden column, if patient_info has
  one, shifts overall latent severity (not item-specific) via a z-scored
  weighted addition. Off unless severity_col is set in config.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Official ASRS-v1.1 Part A shaded-box thresholds (0=Never .. 4=Very Often).
# Items 1-3: threshold = Sometimes (2). Items 4-6: threshold = Often (3).
ITEM_THRESHOLDS = {
    "asrs_q1": 2,
    "asrs_q2": 2,
    "asrs_q3": 2,
    "asrs_q4": 3,
    "asrs_q5": 3,
    "asrs_q6": 3,
}
ITEM_IDS = list(ITEM_THRESHOLDS.keys())

# Items with a well-evidenced age relationship (see module docstring).
# q4 (avoiding/delaying tasks requiring thought) is executive/inattentive in
# character, not hyperactive - intentionally excluded from age adjustment.
HYPERACTIVITY_ITEMS = {"asrs_q5", "asrs_q6"}

# Calibrated by grid search (see calibration note in README) to land within
# ~0.2 percentage points of the 80% / 30% screen-positive targets described
# above, at n~8000 simulated patients per group.
DEFAULT_ADHD_BETA = (3.0, 1.0)  # mean ~0.75, right-skewed -> high latent severity
DEFAULT_CONTROL_BETA = (1.8, 2.5)  # mean ~0.42, left-leaning -> low latent severity
ITEM_NOISE_SD = 0.22  # per-item deviation from latent severity


def latent_severity(n: int, alpha: float, beta: float, rng: np.random.Generator) -> np.ndarray:
    return rng.beta(alpha, beta, size=n)


def severity_to_item_response(
    severity: np.ndarray, rng: np.random.Generator, noise_sd: float = None
) -> np.ndarray:
    """Map a continuous severity value (with per-item noise) to a 0-4 ordinal response."""
    sd = ITEM_NOISE_SD if noise_sd is None else noise_sd
    noisy = severity + rng.normal(0, sd, size=severity.shape)
    noisy = np.clip(noisy, 0, 1)
    # Quantile-style bins: roughly Never/Rarely/Sometimes/Often/Very Often
    bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    return np.digitize(noisy, bins[1:-1])  # returns 0-4


def _zscore(values: np.ndarray) -> np.ndarray:
    std = values.std()
    if std == 0:
        return np.zeros_like(values, dtype=float)
    return (values - values.mean()) / std


def compute_global_severity_shift(
    patient_info: pd.DataFrame, severity_col: str | None, severity_weight: float
) -> np.ndarray:
    """
    Shifts overall latent severity using an optional continuous covariate
    from patient_info (e.g. an existing symptom-burden/severity score).
    Applies equally to all 6 items. Returns zeros if severity_col is unset.
    """
    n = len(patient_info)
    if not severity_col or severity_col not in patient_info.columns:
        return np.zeros(n)
    z = _zscore(patient_info[severity_col].to_numpy(dtype=float))
    return severity_weight * z


def compute_age_hyperactivity_shift(
    patient_info: pd.DataFrame, age_col: str | None, decay_per_decade: float
) -> np.ndarray:
    """
    Older age -> lower severity contribution, applied only to q5/q6 by the
    caller. Centered on the sample's own mean age so the effect is relative,
    not tied to an assumed population mean. Returns zeros if age_col is unset.
    """
    n = len(patient_info)
    if not age_col or age_col not in patient_info.columns:
        return np.zeros(n)
    age = patient_info[age_col].to_numpy(dtype=float)
    centered_decades = (age - age.mean()) / 10.0
    return -decay_per_decade * centered_decades


def compute_sex_hyperactivity_shift(
    patient_info: pd.DataFrame, sex_col: str | None, sex_effect: dict
) -> np.ndarray:
    """
    Off by default (sex_effect values default to 0 - see module docstring for
    why). Applied only to q5/q6 by the caller if enabled.
    """
    n = len(patient_info)
    if not sex_col or sex_col not in patient_info.columns or not sex_effect:
        return np.zeros(n)
    return patient_info[sex_col].map(sex_effect).fillna(0).to_numpy(dtype=float)


def generate(
    patient_info: pd.DataFrame,
    id_col: str,
    label_col: str,
    adhd_value,
    adhd_beta: tuple[float, float],
    control_beta: tuple[float, float],
    seed: int,
    age_col: str | None = None,
    age_hyperactivity_decay_per_decade: float = 0.0,
    sex_col: str | None = None,
    sex_hyperactivity_effect: dict | None = None,
    severity_col: str | None = None,
    severity_weight: float = 0.0,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = len(patient_info)
    is_adhd = (patient_info[label_col] == adhd_value).to_numpy()

    base_severity = np.empty(n)
    base_severity[is_adhd] = latent_severity(is_adhd.sum(), *adhd_beta, rng)
    base_severity[~is_adhd] = latent_severity((~is_adhd).sum(), *control_beta, rng)

    # Global shift applies to every item equally (e.g. an overall severity covariate).
    global_shift = compute_global_severity_shift(patient_info, severity_col, severity_weight)
    severity = np.clip(base_severity + global_shift, 0, 1)

    # Item-specific shifts apply only to the hyperactivity items (q5, q6).
    hyperactivity_shift = compute_age_hyperactivity_shift(
        patient_info, age_col, age_hyperactivity_decay_per_decade
    ) + compute_sex_hyperactivity_shift(patient_info, sex_col, sex_hyperactivity_effect)
    hyperactivity_severity = np.clip(severity + hyperactivity_shift, 0, 1)

    records = {}
    for item in ITEM_IDS:
        item_severity = hyperactivity_severity if item in HYPERACTIVITY_ITEMS else severity
        records[item] = severity_to_item_response(item_severity, rng)

    out = pd.DataFrame(records)
    out.insert(0, id_col, patient_info[id_col].values)

    positive_flags = pd.DataFrame(
        {item: out[item] >= threshold for item, threshold in ITEM_THRESHOLDS.items()}
    )
    out["asrs_positive_item_count"] = positive_flags.sum(axis=1)
    out["asrs_screens_positive"] = out["asrs_positive_item_count"] >= 4
    out["data_source"] = "synthetic"
    out["synthetic_asrs_version"] = "v2"
    return out


def print_calibration_report(out: pd.DataFrame, patient_info: pd.DataFrame, id_col, label_col, adhd_value):
    merged = out.merge(patient_info[[id_col, label_col]], on=id_col)
    for group_name, group_df in [
        ("ADHD", merged[merged[label_col] == adhd_value]),
        ("Control", merged[merged[label_col] != adhd_value]),
    ]:
        rate = group_df["asrs_screens_positive"].mean()
        print(f"  {group_name} (n={len(group_df)}): {rate:.1%} screen positive")


def main():
    parser = argparse.ArgumentParser(
        description="Generate SYNTHETIC ASRS-v1.1 Part A responses calibrated to HYPERAKTIV diagnosis labels."
    )
    parser.add_argument("--patient-info", required=True, help="Path to HYPERAKTIV patient_info.csv")
    parser.add_argument("--output", default="synthetic_asrs_responses.csv")
    parser.add_argument("--id-col", default="id", help="Patient ID column name in patient_info.csv")
    parser.add_argument("--label-col", default="ADHD", help="Diagnosis label column name")
    parser.add_argument(
        "--adhd-value", default="1", help="Value in label-col that indicates an ADHD diagnosis"
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--age-col", default=None, help="Optional age column for hyperactivity-item age adjustment")
    parser.add_argument(
        "--age-decay-per-decade",
        type=float,
        default=0.08,
        help="Severity reduction per decade above sample mean age, applied to q5/q6 only",
    )
    parser.add_argument("--sex-col", default=None, help="Optional sex column (off by default - see docstring)")
    parser.add_argument(
        "--severity-col", default=None, help="Optional continuous severity/symptom-burden covariate"
    )
    parser.add_argument("--severity-weight", type=float, default=0.15)
    args = parser.parse_args()

    path = Path(args.patient_info)
    if not path.exists():
        sys.exit(f"File not found: {path}")

    patient_info = pd.read_csv(path)

    if args.id_col not in patient_info.columns or args.label_col not in patient_info.columns:
        print(f"Columns found in {path.name}: {list(patient_info.columns)}")
        sys.exit(
            f"\n--id-col '{args.id_col}' or --label-col '{args.label_col}' not found above. "
            "Re-run with the correct column names, e.g.:\n"
            f"  python generate_synthetic_asrs.py --patient-info {path} "
            "--id-col <real_id_column> --label-col <real_label_column> --adhd-value <real_adhd_value>"
        )

    # Try to coerce adhd-value to match the column's dtype (handles "1" vs 1 vs "ADHD")
    adhd_value = args.adhd_value
    col_dtype = patient_info[args.label_col].dtype
    if pd.api.types.is_numeric_dtype(col_dtype):
        try:
            adhd_value = col_dtype.type(args.adhd_value)
        except (ValueError, TypeError):
            pass

    out = generate(
        patient_info,
        id_col=args.id_col,
        label_col=args.label_col,
        adhd_value=adhd_value,
        adhd_beta=DEFAULT_ADHD_BETA,
        control_beta=DEFAULT_CONTROL_BETA,
        seed=args.seed,
        age_col=args.age_col,
        age_hyperactivity_decay_per_decade=args.age_decay_per_decade,
        sex_col=args.sex_col,
        sex_hyperactivity_effect=None,  # off by default via CLI - use config.yaml to enable
        severity_col=args.severity_col,
        severity_weight=args.severity_weight,
    )

    out_path = Path(args.output)
    if not out_path.name.startswith("synthetic_"):
        out_path = out_path.with_name(f"synthetic_{out_path.name}")
    out.to_csv(out_path, index=False)

    print(f"Wrote {len(out)} SYNTHETIC ASRS response rows to {out_path}")
    print("Calibration check (target: ADHD ~80% positive, Control ~30% positive):")
    print_calibration_report(out, patient_info, args.id_col, args.label_col, adhd_value)
    print(
        "\nReminder: label this data as synthetic wherever it's used or reported. "
        "See the module docstring for the required disclosure language."
    )


def run_with_config(config: dict) -> pd.DataFrame:
    """
    Programmatic entry point for feature_engineering.py - runs the same
    generation logic as the CLI but driven by configs/config.yaml instead of
    argparse, so it can be called as one step in the larger pipeline.
    """
    cols = config["columns"]
    cal = config["asrs_calibration"]
    cov = cal.get("covariates", {})
    patient_info = pd.read_csv(config["paths"]["patient_info"])

    global ITEM_NOISE_SD
    ITEM_NOISE_SD = cal["item_noise_sd"]

    out = generate(
        patient_info,
        id_col=cols["id_col"],
        label_col=cols["label_col"],
        adhd_value=cols["adhd_value"],
        adhd_beta=tuple(cal["adhd_beta_params"]),
        control_beta=tuple(cal["control_beta_params"]),
        seed=cal["random_seed"],
        age_col=cov.get("age_col"),
        age_hyperactivity_decay_per_decade=cov.get("age_hyperactivity_decay_per_decade", 0.0),
        sex_col=cov.get("sex_col"),
        sex_hyperactivity_effect=cov.get("sex_hyperactivity_effect"),
        severity_col=cov.get("severity_col"),
        severity_weight=cov.get("severity_weight", 0.0),
    )
    out_path = Path(config["paths"]["synthetic_asrs"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    return out


if __name__ == "__main__":
    main()
