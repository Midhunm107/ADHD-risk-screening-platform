# ADHD Insight

## Non-Diagnostic Behavioural Screening Platform

ADHD Insight is a web-based, non-diagnostic behavioural screening platform. It combines an ASRS-based questionnaire, two browser-based cognitive tasks, behavioural feature extraction, an offline machine-learning research pipeline, and a preliminary screening report.

> **Important:** This project does not diagnose ADHD, replace clinical evaluation, or provide medical treatment. Any model result is a preliminary research result only.

## 1. Project Overview

The project investigates whether simple browser-based cognitive tasks can collect useful behavioural measurements for a preliminary screening profile, and whether browser-generated features can be meaningfully compared with the CPT-II features used by an offline-trained model.

The project has two separate parts:

1. **Live web application** — Consent, anonymous assessment sessions, questionnaire, Sustained Attention Task, Go/No-Go Task, behavioural feature extraction, preliminary screening report.
2. **Offline research pipeline** — HYPERAKTIV data loading and validation, feature engineering, exploratory data analysis, model training, ablation study, feature importance analysis, browser-task compatibility analysis.

The live application must not use the offline model until feature compatibility has been scientifically evaluated.

**Out of scope for this project:** admin dashboard, user authentication, audit logging, task configuration UI, anonymized data export, and follow-up/progress tracking across sessions. These add real engineering effort unrelated to the core research question and are deliberately deferred.

## 2. Main Objectives

- Build an accessible browser-based behavioural screening workflow.
- Collect questionnaire and cognitive-task data with informed consent.
- Store live data using anonymous session identifiers.
- Extract behavioural features from raw task trials.
- Study CPT-II, questionnaire, and actigraphy features from HYPERAKTIV.
- Investigate browser-task-to-CPT-II feature compatibility.
- Generate a preliminary behavioural profile.
- Maintain privacy and non-diagnostic safeguards.

## 3. Main Modules

1. **Anonymous Session Management** — unique session token, progress tracking, resume support, timestamps.
2. **Consent Management** — explains purpose and non-diagnostic nature, requires consent before data collection, stores consent version and timestamp.
3. **Questionnaire Module** — displays ASRS-based questions, validates and saves responses, calculates a score.
4. **Sustained Attention Task** — shows stimuli one at a time, records responses, correctness, missed targets, and reaction time.
5. **Go/No-Go Task** — records correct responses, missed Go responses, false alarms, and reaction time.
6. **Feature Extraction** — accuracy, mean/median reaction time, reaction-time variability, missed responses, false alarms, commission and omission errors.
7. **Screening Report** — displays questionnaire and task performance, generates a preliminary behavioural profile, includes a model prediction only when compatibility is established.

## 4. User Workflow

```text
Home
  ↓
Project Explanation
  ↓
Consent
  ↓
Anonymous Session Creation
  ↓
Questionnaire
  ↓
Sustained Attention Task
  ↓
Go/No-Go Task
  ↓
Raw Trial Data Storage
  ↓
Behavioural Feature Extraction
  ↓
Compatibility Check
  ↓
Preliminary Behavioural Profile
  ↓
Screening Report
```

## 5. Machine-Learning Research

The offline pipeline uses the real HYPERAKTIV dataset. Current preliminary ablation results:

| Feature set | Best model | Accuracy |
|---|---|---:|
| CPT-II only | Random Forest | 72.8% |
| CPT-II + questionnaire | XGBoost | 80.5% |
| CPT-II + questionnaire + actigraphy | Logistic Regression | 69.9% |

These are preliminary cross-validated research results on HYPERAKTIV, not clinical diagnostic accuracy. The actigraphy result is reported as a genuine research finding: adding 787 activity features did not improve performance in this small-sample experiment.

## 6. Browser-Task Compatibility

The current HYPERAKTIV model uses CPT-II summary features and questionnaire features. Browser tasks produce different measurements, so the mapping must be checked rather than assumed.

| CPT-II concept | Browser measurement |
|---|---|
| Omissions | Missed targets |
| Commissions | Incorrect responses or false alarms |
| Hit reaction time | Mean reaction time |
| Hit RT variability | Reaction-time variability |
| Perseverative responses | Very fast or impulsive responses |

The compatibility analysis compares definitions, units, ranges, and distributions. If the mapping is valid, a browser-compatible model may be trained. If it is not valid, the system shows a behavioural profile without a model prediction.

## 7. System Architecture

The project uses a modular Flask monolith. Microservices are not required.

```text
User Browser
(HTML/CSS/JavaScript/Bootstrap/Chart.js)
        ↓ HTTP
Flask Application
        ↓
Routes / Blueprints
        ↓
Service Layer
(Session, Questionnaire, Cognitive Tasks,
Feature Extraction, Reports)
        ↓
SQLite Database
        ↓
HTML Templates and Charts
```

The offline pipeline runs separately:

```text
HYPERAKTIV Dataset → Data Loading and Validation → Feature Engineering
→ EDA → Model Training → Cross-validation and Ablation
→ Feature Importance → Compatibility Analysis
```

## 8. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | HTML, CSS, Bootstrap | Pages and layout |
| Browser logic | JavaScript | Questionnaire and cognitive tasks |
| Charts | Chart.js | Report visualisations |
| Backend | Flask | Application and routes |
| Routing | Flask Blueprints | Modular route organisation |
| Database | SQLite | Local data storage |
| Data processing | pandas, NumPy | Cleaning and feature engineering |
| Machine learning | scikit-learn, XGBoost | Training and evaluation |
| Model storage | joblib | Save trained models |
| Version control | Git and GitHub | Collaboration and history |

## 9. Project Structure

```text
adhd-insight/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── adhd_ml_pipeline/
│   ├── data/raw/
│   ├── data/processed/
│   ├── models/
│   ├── reports/
│   └── src/
│       ├── data_loading.py
│       ├── feature_engineering.py
│       ├── eda.py
│       ├── train.py
│       ├── feature_importance.py
│       └── compatibility_analysis.py
│
├── routes/
│   ├── main.py
│   ├── consent.py
│   ├── questionnaire.py
│   ├── cognitive.py
│   └── reports.py
│
├── services/
│   ├── session_service.py
│   ├── feature_service.py
│   └── report_service.py
│
├── models/
│   ├── database.py
│   ├── session.py
│   ├── consent.py
│   ├── cognitive_trial.py
│   └── screening_report.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── consent.html
│   ├── questionnaire.html
│   ├── attention_task.html
│   ├── go_no_go.html
│   └── report.html
│
├── static/
│   ├── css/
│   └── js/
├── instance/adhd_insight.db
└── tests/
```

## 10. Database Tables

- `sessions`: anonymous session token, status, timestamps
- `consents`: consent status, version, timestamp
- `questionnaire_responses`: answers and questionnaire version
- `cognitive_trials`: one row per task trial
- `behavioural_features`: extracted feature values
- `screening_reports`: generated preliminary reports

Live session data and HYPERAKTIV training data remain separate. No unnecessary identifying information is stored.

## 11. Development Roadmap

### Phase 1 — Offline ML pipeline
Data loading and validation, feature engineering, EDA, model training, ablation study, feature importance. *(Complete, ~70%.)*

### Phase 2 — Web foundation
Flask application, homepage, consent page, questionnaire pages, SQLite setup, Blueprint organisation. *(Complete.)*

### Phase 3 — Assessment workflow
Anonymous sessions, consent storage, questionnaire storage, Sustained Attention Task, Go/No-Go Task, raw trial storage.

### Phase 4 — Feature and report layer
Feature extraction, compatibility analysis, preliminary report generation.

### Phase 5 — Testing and documentation
Unit tests, route tests, database tests, cognitive-task tests, end-to-end workflow testing, final report and screenshots.

## 12. Definition of Done

The user can:

1. Open the homepage.
2. Provide consent.
3. Create an anonymous session.
4. Complete the questionnaire.
5. Complete both cognitive tasks.
6. Store raw trial data.
7. Extract behavioural features.
8. Generate and view a preliminary report.

## 13. Instructions for Claude

- Treat this README as the current project direction.
- Do not revert the project to a questionnaire-only website.
- Do not add admin dashboard, authentication, audit logging, task configuration, data export, or follow-up/progress tracking unless explicitly requested later.
- Preserve the existing HYPERAKTIV ML pipeline.
- Use Flask, SQLite, HTML, CSS, JavaScript, Bootstrap, Chart.js, pandas, NumPy, scikit-learn, and XGBoost.
- Use Flask Blueprints for organisation.
- Build one small feature at a time.
- Explain each change before coding.
- Provide exact file names and complete code.
- After each feature, explain how to run and test it.
- Never claim browser-task features are already compatible with the HYPERAKTIV model.
- Keep live data anonymous. Include non-diagnostic disclaimers.
- Implement in this order:

```text
Session Management
→ Consent Storage
→ Questionnaire Storage
→ Sustained Attention
→ Go/No-Go
→ Feature Extraction
→ Screening Report
→ Testing
```

## 14. Immediate Next Task

Build anonymous session management and consent storage.

```text
Homepage
  → Start Assessment
  → Create anonymous session
  → Consent page
  → Save consent in SQLite
  → Redirect to questionnaire
  → Update session status
```
