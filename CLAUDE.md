# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A research-oriented, **non-diagnostic** ADHD screening prototype: a
questionnaire + browser cognitive tasks (Sustained Attention, Go/No-Go) feed
a Flask/SQLite website, alongside a separate, independently reproducible ML
research pipeline on the HYPERAKTIV dataset. Full specs:
`docs/ADHD_Project_Master_Specification.md` and
`docs/ADHD_Insight_Website_Building_Specification.md` — read them before any
cross-cutting or new-module work; this file only summarizes them.

## Project status

Per the master spec's phase plan (§30), **Phases 0-4 are done, Phase 5 has
not started**: repo setup, HYPERAKTIV exploration, the (now-superseded)
synthetic dataset, and the batch feature-engineering pipeline are all in
place, and the ML baseline is a verified result — **80.5% accuracy**
(XGBoost, CPT-II + real questionnaire features, 5-fold stratified CV; see
`adhd_ml_pipeline/README.md` for the full ablation table).

Phase 5 (web foundation: Flask app, homepage, consent, questionnaire,
attention task) and Phases 6-8 (integration, testing, docs for the website)
have **not started** — no `backend/`, `frontend/`, `app.py`, or database
code exists yet. Do not assume any Flask routes, HTML templates, SQLite
schema, or JS task code exist. The only working code is `adhd_ml_pipeline/`.

## Non-negotiable rules (master spec §33, §4, website spec §20-21)

- **No diagnosis claims, anywhere.** Never "you have ADHD" or an
  unqualified probability of having it. Use "preliminary screening
  indication" / "behavioural profile," always with a disclaimer that this
  isn't a substitute for clinical assessment.
- **Never invent results.** No made-up accuracy, participant counts, or
  scientific conclusions. Unmeasured claims are labeled "Planned" or "Not
  yet evaluated," not stated as fact.
- **Synthetic ≠ real.** Any synthetic data/results must be clearly labeled
  and never presented as clinical evidence. `src/asrs_synthesis.py` is a
  leftover from before real questionnaire columns were confirmed in
  `patient_info.csv` — it's unused now, kept only for its calibration
  methodology as reference.
- **HYPERAKTIV features ≠ browser-task features, until proven otherwise.**
  Do not wire a HYPERAKTIV-trained model to future website-generated
  features (attention accuracy, RT, false alarms, etc.) without first
  validating construct/distribution compatibility. If compatibility can't
  be shown, keep the website's behavioural analysis and the HYPERAKTIV ML
  experiment as separate, clearly-labeled components — never force an
  invalid mapping just to make a demo work.
- **No PII/secrets in commits.** No real participant identifiers beyond
  what HYPERAKTIV already anonymizes, no credentials, no `.env` files.
- **Don't redesign without approval.** Flask stays Flask, SQLite stays
  SQLite, classical ML stays classical ML (not deep learning), vanilla
  HTML/JS stays vanilla (not React) — ask before changing any of these, or
  the dataset/cognitive-task scope.
- **Simple + working + tested** over complex + impressive + unfinished.
  Explain what you're about to build before generating many files. Test one
  module at a time, not everything at the end.
- **Anonymous sessions only** for future website work — no login, no
  names/emails unless explicitly required.

## Architecture: two separate data paths

```
PATH A (research, implemented)          PATH B (application, not started)
HYPERAKTIV → preprocessing →            Browser tasks → raw events →
feature extraction → ML models →        feature extraction → screening-
evaluation                              oriented result (Flask + SQLite)
```

These stay architecturally separate (website spec §19) — the ML pipeline
must remain independently reproducible regardless of website state.

## The ML pipeline (`adhd_ml_pipeline/`) — the only implemented component

Real HYPERAKTIV data: CPT-II clinical summary scores, real questionnaire
scores (ASRS/WURS/MADRS/HADS), optional tsfresh actigraphy features. Run
everything below from `adhd_ml_pipeline/`:

```bash
pip install -r requirements.txt

python -m src.data_loading           # sanity-check real column names load
python -m src.feature_engineering    # builds feature_dataset.csv (+ _with_actigraphy)
python -m src.eda                    # group stats + correlation heatmap -> reports/
python -m src.train                  # runs all 3 feature-set ablations, saves best model

python -m pytest tests/ -v           # all tests
python -m pytest tests/test_asrs_synthesis.py -v -k test_name   # single test
```

Flow: `configs/config.yaml` (single source of truth for paths/real column
names) → `data_loading.py` → `feature_engineering.py` → `{eda.py, train.py}`.
Don't hardcode paths/columns in `src/` — add them to the config.

Key details:
- CSVs are **semicolon-delimited**, not comma.
- `feature_engineering.py` left-joins onto `patient_info` (103 patients) as
  the base table; missing data (not every patient completed every
  assessment) is expected, not a bug.
- `train.py`'s three ablations: `cpt_only` / `cpt_questionnaire` (the
  recommended, best-performing set) / `cpt_questionnaire_actigraphy` (known
  to underperform — more tsfresh features than patients). Best model saves
  to `models/best_model.joblib` as `{"model", "scaler", "feature_cols"}` —
  load all three together.
- This dataset's `ASRS` column is the full 18-item checklist, not the
  6-item Part A screener the future website questionnaire would use —
  different instrument/scale, don't conflate them. `AGE` is categorical
  (1-4), not raw years.

## When Phase 5 (web) work starts

Follow the website spec's structure (`app.py`/`models/`/`routes/`/
`services/`/`templates/`/`static/`, Flask + SQLAlchemy + SQLite) and build
one milestone at a time in order: Flask foundation → session/consent →
questionnaire → attention task → Go/No-Go → feature extraction → results
dashboard → ML integration (only once feature compatibility is validated).
Store raw trial events, not just derived scores.
