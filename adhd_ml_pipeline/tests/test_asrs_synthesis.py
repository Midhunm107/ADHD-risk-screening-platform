"""
Verifies the synthetic ASRS generator's calibration lands near its documented
targets (80% ADHD / 30% control screen-positive rate) at a large enough n
that sampling noise doesn't mask a real miscalibration.

Run with: python -m pytest tests/test_asrs_synthesis.py -v
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.asrs_synthesis import DEFAULT_ADHD_BETA, DEFAULT_CONTROL_BETA, generate


def _mock_patient_info(n_adhd: int, n_control: int) -> pd.DataFrame:
    n = n_adhd + n_control
    return pd.DataFrame({"id": range(1, n + 1), "ADHD": [1] * n_adhd + [0] * n_control})


def test_adhd_group_calibration_near_target():
    patient_info = _mock_patient_info(n_adhd=2000, n_control=2000)
    out = generate(
        patient_info,
        id_col="id",
        label_col="ADHD",
        adhd_value=1,
        adhd_beta=DEFAULT_ADHD_BETA,
        control_beta=DEFAULT_CONTROL_BETA,
        seed=1,
    )
    merged = out.merge(patient_info, on="id")
    adhd_rate = merged[merged["ADHD"] == 1]["asrs_screens_positive"].mean()
    assert 0.75 <= adhd_rate <= 0.85, f"ADHD screen-positive rate {adhd_rate:.3f} outside target band"


def test_control_group_calibration_near_target():
    patient_info = _mock_patient_info(n_adhd=2000, n_control=2000)
    out = generate(
        patient_info,
        id_col="id",
        label_col="ADHD",
        adhd_value=1,
        adhd_beta=DEFAULT_ADHD_BETA,
        control_beta=DEFAULT_CONTROL_BETA,
        seed=1,
    )
    merged = out.merge(patient_info, on="id")
    control_rate = merged[merged["ADHD"] == 0]["asrs_screens_positive"].mean()
    assert 0.25 <= control_rate <= 0.35, f"Control screen-positive rate {control_rate:.3f} outside target band"


def test_output_is_labeled_synthetic():
    patient_info = _mock_patient_info(n_adhd=10, n_control=10)
    out = generate(
        patient_info,
        id_col="id",
        label_col="ADHD",
        adhd_value=1,
        adhd_beta=DEFAULT_ADHD_BETA,
        control_beta=DEFAULT_CONTROL_BETA,
        seed=1,
    )
    assert (out["data_source"] == "synthetic").all()


def test_age_covariate_lowers_hyperactivity_items_only():
    """Older patients should score lower on q5/q6 (hyperactivity) specifically,
    with inattention items (q1) essentially unaffected - matches the
    literature cited in the module docstring."""
    n = 4000
    # AGE alternates independently of ADHD label so the two aren't confounded -
    # each diagnosis group has an equal mix of young (25) and old (60) patients.
    patient_info = pd.DataFrame(
        {
            "id": range(n),
            "ADHD": ([1] * (n // 2) + [0] * (n // 2)),
            "AGE": ([25, 60] * (n // 2)),
        }
    )
    out = generate(
        patient_info,
        id_col="id",
        label_col="ADHD",
        adhd_value=1,
        adhd_beta=DEFAULT_ADHD_BETA,
        control_beta=DEFAULT_CONTROL_BETA,
        seed=1,
        age_col="AGE",
        age_hyperactivity_decay_per_decade=0.08,
    )
    merged = out.merge(patient_info[["id", "AGE"]], on="id")
    young_q5 = merged[merged["AGE"] == 25]["asrs_q5"].mean()
    old_q5 = merged[merged["AGE"] == 60]["asrs_q5"].mean()
    young_q1 = merged[merged["AGE"] == 25]["asrs_q1"].mean()
    old_q1 = merged[merged["AGE"] == 60]["asrs_q1"].mean()

    assert young_q5 - old_q5 > 0.2, "Expected meaningfully higher q5 (hyperactivity) in younger group"
    assert abs(young_q1 - old_q1) < 0.15, "q1 (inattention) should be ~unaffected by age covariate"


def test_sex_covariate_off_by_default():
    """Sex should have zero effect unless explicitly configured, per the
    clinical-population evidence cited in the module docstring."""
    n = 200
    patient_info = pd.DataFrame(
        {"id": range(n), "ADHD": [1] * (n // 2) + [0] * (n // 2), "SEX": ["M", "F"] * (n // 2)}
    )
    out = generate(
        patient_info,
        id_col="id",
        label_col="ADHD",
        adhd_value=1,
        adhd_beta=DEFAULT_ADHD_BETA,
        control_beta=DEFAULT_CONTROL_BETA,
        seed=1,
        sex_col="SEX",
        sex_hyperactivity_effect=None,  # explicitly off
    )
    merged = out.merge(patient_info[["id", "SEX"]], on="id")
    m_rate = merged[merged["SEX"] == "M"]["asrs_screens_positive"].mean()
    f_rate = merged[merged["SEX"] == "F"]["asrs_screens_positive"].mean()
    assert abs(m_rate - f_rate) < 0.15, "Sex should have no systematic effect when disabled"


def test_item_scores_within_valid_range():
    patient_info = _mock_patient_info(n_adhd=50, n_control=50)
    out = generate(
        patient_info,
        id_col="id",
        label_col="ADHD",
        adhd_value=1,
        adhd_beta=DEFAULT_ADHD_BETA,
        control_beta=DEFAULT_CONTROL_BETA,
        seed=1,
    )
    item_cols = [c for c in out.columns if c.startswith("asrs_q")]
    for col in item_cols:
        assert out[col].between(0, 4).all(), f"{col} has values outside 0-4"
