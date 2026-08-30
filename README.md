# ADHD Risk Screening and Cognitive Behaviour Analysis Platform

A research-oriented web platform for **preliminary, non-clinical ADHD risk
screening**, combining a self-report questionnaire, browser-based cognitive
tasks, and a machine-learning model trained on real clinical data.

> **This platform is not a diagnostic tool.** It is a screening and awareness
> aid only. Anyone with concerns about ADHD should consult a qualified
> healthcare professional.

---

## Project Status

| Phase | Description | Status |
|---|---|---|
| 0 | Repository setup | ✅ Complete |
| 1 | Dataset exploration (HYPERAKTIV) | ✅ Complete |
| 2 | Synthetic dataset (pipeline testing only) | ✅ Complete |
| 3 | Batch processing pipeline | ✅ Complete |
| 4 | ML baseline & evaluation | ✅ Complete — verified 80.5% accuracy |
| 5 | Web foundation (Flask, tasks, UI) | 🔜 In progress |
| 6 | Integration | ⏳ Not started |
| 7 | Testing & evaluation | ⏳ Not started |
| 8 | Documentation & final report | ⏳ Not started |

## Verified Research Result

Trained and evaluated on the real [HYPERAKTIV dataset](https://datasets.simula.no/hyperaktiv/)
(103 participants: 51 ADHD, 52 controls), using stratified k-fold cross-validation.

| Feature Set | Best Model | Accuracy | Sensitivity | Specificity |
|---|---|---|---|---|
| CPT-II only | Random Forest | 72.8% | 74.4% | 70.7% |
| CPT-II + Questionnaire (ASRS/WURS/MADRS/HADS) | **XGBoost** | **80.5%** | 78.2% | 82.5% |
| CPT-II + Questionnaire + Actigraphy (787 features) | Logistic Regression | 70.0% | 64.5% | 75.1% |

Adding real questionnaire data measurably improved accuracy. Adding raw
actigraphy features on only 103 patients *reduced* accuracy — a reported
dimensionality finding, not a discarded result.

All results above are independently reproducible from a clean run — see
[Running the ML Pipeline](#running-the-ml-pipeline) below.

## Known Open Research Question

The ML model above is trained on clinical CPT-II test data, which is **not
feature-compatible** with the lightweight browser-based cognitive tasks this
platform will use. Resolving this (redesigning tasks to output comparable
raw metrics, and retraining a browser-compatible model variant) is active,
ongoing work — see `docs/ADHD_Project_Master_Specification.md`, Section 40.

## Repository Structure

```
├── adhd_ml_pipeline/     # Verified ML pipeline (data loading, features, training)
│   ├── data/raw/         # HYPERAKTIV files — NOT committed, see data/raw/README.md
│   ├── src/              # Pipeline source code
│   ├── models/           # Saved trained model artifacts
│   ├── reports/          # Evaluation reports & figures
│   └── tests/            # Unit tests
├── docs/                 # Specifications, literature review, project diary
├── requirements.txt
└── .gitignore
```

## Running the ML Pipeline

```bash
cd adhd_ml_pipeline
pip install -r requirements.txt
python -m src.data_loading
python -m src.feature_engineering
python -m src.train
```

See `adhd_ml_pipeline/data/raw/README.md` for where to obtain the HYPERAKTIV
dataset — raw patient data is intentionally excluded from this repository.

## Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, JavaScript, Chart.js
- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn, XGBoost, pandas
- **Database:** SQLite
- **Version Control:** Git + GitHub

## Dataset Citation

S. A. Hicks et al., "HYPERAKTIV: An Activity Dataset from Adult Patients
with Attention-Deficit/Hyperactivity Disorder (ADHD)," in *Proc. 12th ACM
Multimedia Systems Conf. (MMSys '21)*, 2021, pp. 314–319.
Licensed CC BY-NC 4.0 — used here for academic research only.

## Team

- **Midhun** — ML pipeline, backend
- **Asif Mohammed Ali** — frontend, cognitive task UI

MCA Mini Project, Department of Computer Applications.