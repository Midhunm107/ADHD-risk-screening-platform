# ADHD ML/Screening Pipeline (HYPERAKTIV, real data)

Trains LR/RF/XGBoost on the real HYPERAKTIV dataset: CPT-II clinical summary
scores, real ADHD questionnaire data (ASRS/WURS/MADRS/HADS), and optional
tsfresh actigraphy features. **No synthetic data is used** - see "About the
earlier synthetic ASRS work" below for why that changed.

## Real results (5-fold stratified CV, this exact repo, your uploaded files)

| Feature set | Best model | Accuracy |
|---|---|---|
| CPT-II only | Random Forest | 72.8% (matches your established 72.7% baseline) |
| CPT-II + real questionnaire (ASRS/WURS/MADRS/HADS) | XGBoost | **80.5%** |
| + 787 actigraphy features | Logistic Regression | 69.9% (worse than baseline) |

This is a coherent, defensible story for your report: the CPT-only run
replicates prior work almost exactly (72.8% vs 72.7%), adding real
questionnaire data genuinely helps, and adding the high-dimensional raw
actigraphy features hurts - consistent with your prior finding that 787
tsfresh features on ~85 patients is a severe dimensionality mismatch.

## About the earlier synthetic ASRS work

Earlier in this project, `patient_info.csv`'s real columns hadn't been
checked, so `src/asrs_synthesis.py` was built to *simulate* ASRS responses
calibrated to the diagnosis label. Once the real files were uploaded, it
turned out `patient_info.csv` already has real `ASRS`, `WURS`, `MADRS`,
`HADS_A`, `HADS_D` columns - actual measured clinical assessments. That
synthetic module is **no longer used** in this pipeline; it's kept in
`src/` only as a reference for the calibration methodology, in case you
ever need to simulate a questionnaire feature that genuinely doesn't exist
in a dataset. Don't use it here - the real columns are simply better.

One real caveat worth naming in your report: the real `ASRS` column here is
the full **18-item checklist total** (range 6-68 in this sample), not the
6-item Part A screener used elsewhere in this project (e.g. the Flutter
app's live questionnaire, or the backend's `ASRS_PART_A_ITEMS`). Different
instrument, different scale - don't treat them as interchangeable.

## Real file schema (confirmed from your uploads, not guessed)

All three HYPERAKTIV files are **semicolon-delimited**, not comma:

- **`patient_info.csv`** (103 rows) - `ID`, `SEX`, `AGE` (coded 1-4, likely
  quartile-binned for anonymization - not raw years), `ADHD` (0/1 label),
  real questionnaire scores (`ASRS`, `WURS`, `MADRS`, `HADS_A`, `HADS_D`),
  psychiatric comorbidity flags, medication flags, and a `CPT_II` completion
  flag (0/1).
- **`CPT_II_ConnersContinuousPerformanceTest.csv`** (99 rows - only patients
  who completed it, confirmed to exactly match `patient_info`'s `CPT_II`
  flag) - `ID` + 720 raw per-trial columns (`Trial1`/`Response1`..`Trial360`/
  `Response360`, excluded from features) + ~60 real summary/clinical columns
  (T-scores, raw scores, percentiles, confidence indices - these are what
  the model actually trains on).
- **`features.csv`** (116 rows) - `ID` + 787 already-computed tsfresh
  actigraphy (`ACC__`) features. 85 of your 103 patients have a row here
  (103 - 18 missing = 85, matching your established figure exactly); the
  other 31 IDs (210-240 range) fall outside `patient_info`'s ID range and
  are correctly excluded once merges start from `patient_info` as the base
  table.

## Project layout

```
configs/config.yaml         # real column names, confirmed against your files
src/
  data_loading.py             # loads all three real files, sep=';'
  asrs_synthesis.py            # UNUSED for this dataset - see above
  feature_engineering.py        # builds cpt_only / cpt+questionnaire / +actigraphy datasets
  eda.py                         # group summary stats + correlation heatmap
  train.py                        # LR/RF/XGBoost across all three feature sets
tests/test_asrs_synthesis.py    # tests for the (now unused) synthetic module
```

## Setup

```bash
pip install -r requirements.txt
```

Copy your three real files into `data/raw/`:
`patient_info.csv`, `CPT_II_ConnersContinuousPerformanceTest.csv`,
`features.csv` (exact names matter - `config.yaml` points at these).

```bash
python -m src.data_loading           # sanity-check real column names load correctly
python -m src.feature_engineering     # builds both feature_dataset.csv variants
python -m src.eda                      # summary stats + correlation heatmap
python -m src.train                     # runs all three feature-set ablations
```

`train.py` saves the best model from the `cpt_questionnaire` run (the
recommended feature set) to `models/best_model.joblib`.

## Known data quirks worth documenting in your report

- **Missing data is real and expected**: not every patient completed every
  assessment (7 missing ASRS, 13 missing MADRS, etc. - see
  `data_loading.py`'s docstrings). Median imputation is used; consider
  reporting how many patients had complete vs imputed data.
- **6 tsfresh columns are 100% NaN** for every subject (e.g.
  `friedrich_coefficients`, `max_langevin_fixed_point`) - these are dropped
  automatically in `train.py`, not imputed, since a median of nothing is
  undefined.
- **`AGE` is categorical (1-4), not raw years** - likely binned for
  anonymization. Don't treat it as a continuous variable without checking
  this against the original HYPERAKTIV paper's age-binning scheme.

## Run tests

```bash
python -m pytest tests/ -v
```
