# ADHD Risk Screening and Cognitive Behaviour Analysis Platform

## Master Project Specification & Implementation Guide for Claude Code

**Project type:** MCA Mini Project / Research-oriented software project\
**Team:** Midhun M. Pillai & Asif Mohammed Ali\
**Primary goal:** Build a browser-based, preliminary, non-clinical ADHD
screening research prototype using questionnaire responses,
browser-based cognitive-task behaviour, a research dataset (HYPERAKTIV),
a reproducible data-processing pipeline, and classical machine learning.

------------------------------------------------------------------------

# 1. PURPOSE OF THIS DOCUMENT

This is the **master context document for the project**.

It is intended to be given to an AI coding agent such as Claude Code at
the beginning of development so that the agent understands:

-   what the project is trying to achieve;
-   what has already been decided;
-   what is in scope and out of scope;
-   how the research dataset and application data relate;
-   how the synthetic dataset is to be used;
-   the proposed architecture;
-   the technology stack;
-   the implementation order;
-   the expected repository structure;
-   what must not be changed without approval;
-   what should be treated as research evidence versus
    software-development validation.

The project has a short implementation window. Therefore, **simplicity,
reproducibility, modularity and a demonstrable working system are more
important than adding unnecessary features**.

Claude Code should use this document as the high-level source of truth
for implementation unless the project guide later approves a scope
change.

------------------------------------------------------------------------

# 2. PROJECT TITLE

## ADHD Risk Screening and Cognitive Behaviour Analysis Platform

Alternative short name used in code/repository:

`adhd-screening-platform`

------------------------------------------------------------------------

# 3. PROJECT VISION

The project investigates whether a lightweight browser-based platform
can collect behavioural measurements from short cognitive tasks, combine
them with questionnaire information, and support **preliminary ADHD risk
screening research** using machine-learning techniques.

The platform is **not a diagnostic system**.

The intended workflow is:

``` text
User
  ↓
Consent / Disclaimer
  ↓
ADHD Screening Questionnaire
  ↓
Browser-Based Cognitive Assessment
  ├── Sustained Attention
  └── Go/No-Go
  ↓
Behavioural Metrics
  ↓
Feature Extraction
  ↓
Screening / ML Analysis
  ↓
Preliminary Screening-Oriented Profile
  ↓
Results + Explanation + Disclaimer
```

An optional N-Back task may be added later if implementation time
permits.

------------------------------------------------------------------------

# 4. IMPORTANT SCOPE DECISIONS

These decisions are intentional and should be preserved.

## 4.1 No large volunteer recruitment

The team cannot realistically recruit 150 or more volunteers within the
available project duration.

Therefore:

-   do not make large-scale participant recruitment a core dependency;
-   do not create fake claims about real participants;
-   do not present synthetic participants as human participants;
-   use existing research data for the ML research component;
-   use synthetic data to validate software/data-processing pipelines
    where appropriate.

## 4.2 HYPERAKTIV is the primary research dataset

HYPERAKTIV is the main existing dataset being investigated for the ML
research component.

The project documentation describes it as containing:

-   103 participants in total;
-   51 diagnosed ADHD participants;
-   52 clinical controls;
-   motor/activity data;
-   heart-rate data for a subset;
-   computerized CPT-II data;
-   demographic and clinical attributes.

The dataset is associated with the HYPERAKTIV research paper by Hicks et
al.

## 4.3 Synthetic dataset is for development and pipeline validation

Synthetic data is introduced because the team needs to develop and
demonstrate:

``` text
data generation
    ↓
preprocessing
    ↓
feature extraction
    ↓
batch processing
    ↓
ML pipeline execution
```

Synthetic data must be clearly labelled as:

> Synthetic data generated for software pipeline development and
> testing. It does not represent real participants and must not be
> presented as clinical evidence.

Synthetic data may be used to verify that code works, but model
performance obtained only from synthetic data must not be described as
clinical performance.

## 4.4 No diagnosis claim

The website must never tell a user:

> "You have ADHD."

Preferred language:

-   preliminary screening profile;
-   screening indication;
-   behavioural profile;
-   higher/lower screening indication;
-   research result;
-   non-clinical result.

Every result page should contain a clear disclaimer that the system is
not a substitute for professional clinical assessment or diagnosis.

## 4.5 Keep the first implementation small

Core cognitive tasks:

1.  Sustained Attention
2.  Go/No-Go

Optional:

3.  N-Back

Do not allow N-Back, NLP, deployment, authentication, advanced
dashboards, or other optional features to delay the core system.

------------------------------------------------------------------------

# 5. RESEARCH MOTIVATION

ADHD screening can involve subjective self-report and clinical
assessment. Existing computational approaches may also rely on wearable
sensors or specialized data-collection environments.

The project's research direction is to investigate a more accessible
browser-based approach in which a user can complete short cognitive
tasks without dedicated hardware.

The central research question is:

> Can behavioural measurements obtained from short browser-based
> cognitive tasks, together with questionnaire responses, be processed
> into useful features for preliminary ADHD screening research?

This should be treated as an investigation, not as a claim that the
platform can replace clinical diagnosis.

------------------------------------------------------------------------

# 6. PROBLEM STATEMENT

A concise version:

> Existing ADHD screening approaches may rely heavily on subjective
> self-report or specialized assessment environments. This project
> investigates whether behavioural measurements obtained from short
> browser-based cognitive tasks, together with a standardized screening
> questionnaire, can be processed using machine-learning techniques to
> provide an accessible preliminary screening profile.

------------------------------------------------------------------------

# 7. RESEARCH GAP

The project documentation identifies the following practical gap:

> Existing computational ADHD approaches may depend on wearable sensor
> hardware, physiological measurements, or supervised
> clinical/semi-clinical environments. A lightweight browser-based
> behavioural assessment can be investigated as a more accessible
> alternative for preliminary screening research.

The project therefore focuses on:

-   no dedicated wearable hardware;
-   browser-based interaction;
-   millisecond-level response timing using JavaScript;
-   reproducible behavioural feature extraction;
-   classical ML experimentation;
-   a web interface for demonstrating the research workflow.

Important: the project should not claim that browser-based tasks are
clinically equivalent to professional assessment.

------------------------------------------------------------------------

# 8. RESEARCH DATASET --- HYPERAKTIV

## 8.1 Dataset role

HYPERAKTIV is the primary dataset for the research/ML component.

Conceptually:

``` text
HYPERAKTIV
    ↓
Data understanding
    ↓
Data cleaning
    ↓
Batch processing
    ↓
Feature extraction
    ↓
Feature selection
    ↓
Train / validation / test
    ↓
ML models
    ↓
Evaluation
```

## 8.2 Dataset characteristics

According to the current project documentation:

  Attribute             Current understanding
  --------------------- ------------------------------------
  Total participants    103
  ADHD participants     51
  Clinical controls     52
  Main data             Motor/activity, heart rate, CPT-II
  Heart-rate coverage   80 of 103 participants
  Dataset role          Primary research/ML dataset

## 8.3 Important rule

Do not assume that every feature in HYPERAKTIV can be directly produced
by the browser tasks.

For example:

HYPERAKTIV may contain:

``` text
motor activity
heart rate
CPT-II
clinical/demographic variables
```

while the website may generate:

``` text
questionnaire score
attention accuracy
attention reaction time
Go/No-Go accuracy
false-alarm rate
reaction-time variability
```

These are not automatically the same feature space.

Therefore, **do not silently feed website-generated task features into a
model trained on incompatible HYPERAKTIV features**.

The integration strategy must be validated before claiming that the web
user's feature vector is directly compatible with the HYPERAKTIV-trained
model.

------------------------------------------------------------------------

# 9. TWO DATA PATHS

This is one of the most important architectural concepts.

## PATH A --- Research / Existing Dataset

``` text
HYPERAKTIV
    ↓
Raw research data
    ↓
Preprocessing
    ↓
Batch processing
    ↓
Feature extraction
    ↓
ML-ready dataset
    ↓
Model training
    ↓
Evaluation
```

Purpose:

> Research experimentation and benchmarking.

## PATH B --- Development / Synthetic Data

``` text
Synthetic records
    ↓
Batch processing
    ↓
Preprocessing
    ↓
Feature extraction
    ↓
Pipeline validation
    ↓
Software testing
```

Purpose:

> Verify that the technical pipeline works before suitable
> application-level real data is available.

These two paths must be clearly separated in code and documentation.

------------------------------------------------------------------------

# 10. APPLICATION DATA PATH

The browser application creates a third conceptual flow:

``` text
User
  ↓
Questionnaire
  ↓
Questionnaire score
  ↓
Cognitive task
  ↓
Raw event-level responses
  ↓
Behavioural feature extraction
  ↓
User feature vector
  ↓
Analysis / validated model integration
  ↓
Screening-oriented result
```

The application must store raw task events or sufficient structured data
so that features can be recalculated later.

Do not store only a final score if the raw response information can
reasonably be retained.

------------------------------------------------------------------------

# 11. COGNITIVE TASKS

## 11.1 Sustained Attention

Purpose:

> Measure the user's ability to maintain attention over time.

Basic design:

``` text
START
  ↓
Instructions
  ↓
Stimulus appears
  ↓
User responds only to target stimulus
  ↓
Record response + timestamp
  ↓
Repeat for a defined number of trials
  ↓
Calculate behavioural metrics
```

Example metrics:

-   total trials;
-   target trials;
-   correct responses;
-   missed targets;
-   false responses;
-   accuracy;
-   mean reaction time;
-   median reaction time;
-   reaction-time standard deviation;
-   reaction-time variability;
-   performance across time blocks.

The original project document proposes presenting letters one at a time
and asking the user to respond to a target such as "X".

## 11.2 Go/No-Go

Purpose:

> Measure response inhibition / impulsive responding.

Basic design:

``` text
START
  ↓
Instructions
  ↓
GO stimulus → user should respond
NO-GO stimulus → user should withhold response
  ↓
Record response and timing
  ↓
Repeat
  ↓
Calculate behavioural metrics
```

Example metrics:

-   Go accuracy;
-   No-Go accuracy;
-   false alarms;
-   missed Go responses;
-   mean reaction time;
-   median reaction time;
-   reaction-time variability;
-   total trials.

## 11.3 N-Back --- OPTIONAL

Purpose:

> Working-memory-related behavioural measurement.

Only implement after the core questionnaire, Sustained Attention and
Go/No-Go modules are stable.

Do not let N-Back delay the project.

------------------------------------------------------------------------

# 12. QUESTIONNAIRE MODULE

The questionnaire is the self-report component.

Conceptual distinction:

``` text
Questionnaire
    ↓
"What symptoms does the user report?"

Cognitive tasks
    ↓
"How does the user perform on behavioural tasks?"
```

The project documentation references the WHO Adult ADHD Self-Report
Scale (ASRS) as a foundational screening instrument.

Implementation requirements:

-   use an appropriately sourced and documented questionnaire;
-   do not modify a validated instrument casually;
-   preserve item wording/response mapping according to the chosen
    instrument and permitted use;
-   calculate the questionnaire score according to the documented
    scoring procedure;
-   store the response data;
-   clearly label it as screening/self-report information;
-   do not treat the questionnaire score alone as a diagnosis.

If licensing, reproduction or exact item display needs confirmation,
consult the guide before copying a full validated instrument into the
public-facing application.

------------------------------------------------------------------------

# 13. FEATURE EXTRACTION

The feature extraction layer converts raw event-level data into
numerical variables.

Example:

``` text
Raw event data
    ↓
timestamp
stimulus
expected_response
actual_response
response_time
trial_type
    ↓
Feature extraction
    ↓
{
  accuracy,
  mean_rt,
  median_rt,
  rt_std,
  missed_targets,
  false_responses,
  false_alarm_rate
}
```

A key design principle:

> Keep feature extraction deterministic and reusable.

The same feature-extraction function should be usable for:

-   synthetic data;
-   development/test data;
-   future real application data.

------------------------------------------------------------------------

# 14. BATCH PROCESSING PIPELINE

The project should support batch processing rather than manually
processing individual records.

Example:

``` text
data/raw/
    participant_001.csv
    participant_002.csv
    participant_003.csv
    ...
            ↓
batch_process.py
            ↓
preprocess.py
            ↓
feature_extraction.py
            ↓
data/processed/features.csv
```

Expected behaviour:

``` text
Loading input data...
Records found: N

Validating schema...
Cleaning data...
Handling missing/invalid values...
Extracting features...
Saving processed dataset...

Output:
data/processed/features.csv
```

The pipeline should:

1.  load data;
2.  validate expected columns;
3.  handle missing values according to documented rules;
4.  normalize/clean values where appropriate;
5.  calculate features;
6.  preserve participant/session identifiers;
7.  save deterministic output;
8.  log errors clearly.

Do not silently discard records.

------------------------------------------------------------------------

# 15. SYNTHETIC DATA GENERATION

Synthetic data should mimic the **schema**, not pretend to reproduce
clinical reality.

Recommended example schema for application-level pipeline development:

``` text
participant_id
questionnaire_score
attention_accuracy
attention_mean_rt
attention_rt_std
attention_missed_targets
attention_false_responses
gonogo_accuracy
gonogo_mean_rt
gonogo_false_alarms
gonogo_missed_go
label
```

Potential label convention:

``` text
0 = control-like synthetic record
1 = ADHD-like synthetic record
```

However, labels must be explicitly documented as synthetic labels.

The generator should be deterministic when a random seed is provided.

Example conceptual API:

``` python
generate_synthetic_dataset(
    n_samples=1000,
    random_state=42
)
```

Do not create unrealistic values without documenting the assumptions.

Synthetic distributions should be treated as development assumptions,
not clinical facts.

------------------------------------------------------------------------

# 16. MACHINE LEARNING PLAN

## Primary model

Start with:

> Random Forest Classifier

Reason:

-   beginner-friendly;
-   strong classical baseline;
-   handles nonlinear relationships;
-   works well with mixed numerical features;
-   easy to inspect;
-   suitable for a mini-project research comparison.

## Baseline/comparison model

If time permits:

-   Logistic Regression

Optional later:

-   XGBoost

Do not add many models simply to increase complexity.

------------------------------------------------------------------------

# 17. ML PIPELINE

Recommended sequence:

``` text
Processed dataset
      ↓
Separate features and label
      ↓
Data validation
      ↓
Train/test split
      ↓
Preprocessing fitted on training data only
      ↓
Model training
      ↓
Validation / cross-validation
      ↓
Test evaluation
      ↓
Metrics
      ↓
Save model
```

For classification evaluation, report at least:

-   accuracy;
-   precision;
-   recall;
-   F1-score;
-   confusion matrix.

Where appropriate, also report:

-   ROC-AUC.

Because the dataset is relatively small, avoid making strong claims from
one arbitrary train/test split.

Prefer cross-validation for research comparison where appropriate.

------------------------------------------------------------------------

# 18. DATA LEAKAGE PREVENTION

This is a high-priority research requirement.

Do not:

-   fit preprocessing on the complete dataset before splitting;
-   use test-set information during feature selection;
-   duplicate participant records across train and test;
-   create synthetic copies of test participants;
-   report training accuracy as model performance.

If multiple records/windows come from the same participant,
participant-level separation must be considered to avoid leakage.

------------------------------------------------------------------------

# 19. MODEL OUTPUT

The model may internally output:

``` text
0 / 1
```

or probability:

``` text
P(class = 1)
```

But the UI should translate this carefully.

Example:

``` text
Preliminary Screening Profile

The current analysis indicates a higher screening indication
based on the features provided.

This is NOT a diagnosis of ADHD.
```

Avoid:

``` text
"You have ADHD."
```

Avoid:

``` text
"95% chance that you have ADHD."
```

unless there is a scientifically and clinically justified probability
interpretation. A raw classifier probability should not automatically be
presented as an individual's medical probability.

------------------------------------------------------------------------

# 20. SYSTEM ARCHITECTURE

The preferred architecture is:

``` text
                         ┌──────────────────────┐
                         │      USER / WEB       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Consent / Disclaimer │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Questionnaire     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Cognitive Assessment │
                         └──────────┬───────────┘
                                    │
                       ┌────────────┴────────────┐
                       ▼                         ▼
              Sustained Attention           Go / No-Go
                       │                         │
                       └────────────┬────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Behavioural Metrics  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Feature Extraction  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ ML / Analysis Layer  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Screening-Oriented   │
                         │      Result          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Results Dashboard    │
                         │ + Explanation        │
                         │ + Disclaimer         │
                         └──────────────────────┘
```

------------------------------------------------------------------------

# 21. RESEARCH DATA PIPELINE ARCHITECTURE

Separate from the website:

``` text
                  HYPERAKTIV
                      │
                      ▼
               Raw Data Loader
                      │
                      ▼
                Data Validator
                      │
                      ▼
               Preprocessing
                      │
                      ▼
              Batch Processing
                      │
                      ▼
             Feature Extraction
                      │
                      ▼
              Feature Selection
                      │
                      ▼
                ML Training
                      │
                      ▼
                 Evaluation
                      │
                      ▼
             Research Results
```

------------------------------------------------------------------------

# 22. SYNTHETIC DEVELOPMENT PIPELINE

``` text
              Synthetic Generator
                      │
                      ▼
               synthetic_raw.csv
                      │
                      ▼
                Validation
                      │
                      ▼
                Preprocessing
                      │
                      ▼
              Feature Extraction
                      │
                      ▼
                features.csv
                      │
                      ▼
               Pipeline Tests
```

This pipeline is primarily for software development.

------------------------------------------------------------------------

# 23. APPLICATION ARCHITECTURE

``` text
Browser
  │
  │ HTTP / JSON
  ▼
Flask Backend
  │
  ├── Questionnaire routes
  ├── Cognitive-task routes
  ├── Session handling
  ├── Feature processing
  ├── Result handling
  │
  ├──────────────► SQLite
  │
  └──────────────► ML service/module
                         │
                         ▼
                     Saved model
```

Do not over-engineer the backend.

------------------------------------------------------------------------

# 24. TECHNOLOGY STACK

## Frontend

-   HTML5
-   CSS3
-   JavaScript
-   Bootstrap
-   Chart.js

JavaScript is important because cognitive tasks need accurate
client-side event timing and keyboard/mouse response capture.

## Backend

-   Python
-   Flask

## Data processing

-   pandas
-   NumPy

## Machine learning

-   scikit-learn

## Database

-   SQLite

## Version control

-   Git
-   GitHub

## Optional NLP

-   spaCy

The NLP module is supplementary and should not block the core project.

------------------------------------------------------------------------

# 25. OPTIONAL NLP / RESEARCH INSIGHTS MODULE

The original project concept contains a supplementary text-analysis
component.

Purpose:

> Analyze public ADHD-related text or research abstracts to identify
> commonly discussed symptom themes and provide contextual research
> insights.

Possible pipeline:

``` text
Text source
    ↓
Collection
    ↓
Cleaning
    ↓
spaCy tokenisation
    ↓
POS / NER where useful
    ↓
Keyword/theme extraction
    ↓
Aggregation
    ↓
insights.json
    ↓
Website visualization
```

Possible output:

``` json
{
  "attention": 120,
  "forgetfulness": 82,
  "impulsivity": 75,
  "hyperactivity": 69
}
```

However:

-   it is not the ADHD prediction model;
-   it should not be used to diagnose users;
-   it should not consume time needed for the core system;
-   the exact text source must be decided and ethically/legally
    appropriate;
-   research paper abstracts are currently the safer proposed source
    than forum content.

If time is limited, **defer this module**.

------------------------------------------------------------------------

# 26. DATABASE DESIGN

A simple SQLite database is sufficient.

Possible schema:

## sessions

``` text
id
session_id
created_at
completed
```

## questionnaire_responses

``` text
id
session_id
question_id
response
created_at
```

## cognitive_trials

``` text
id
session_id
task_type
trial_number
stimulus
expected_response
actual_response
reaction_time_ms
correct
timestamp
```

## assessment_summary

``` text
id
session_id
questionnaire_score
attention_accuracy
attention_mean_rt
attention_rt_std
attention_missed_targets
attention_false_responses
gonogo_accuracy
gonogo_mean_rt
gonogo_false_alarms
created_at
```

This design preserves raw task events while also allowing derived
summaries.

------------------------------------------------------------------------

# 27. PRIVACY DESIGN

The project is research-oriented and involves sensitive behavioural
information.

Therefore:

-   do not collect unnecessary personally identifying information;
-   use a generated session ID instead of names by default;
-   do not require email/phone unless explicitly needed;
-   do not store passwords because authentication is not required;
-   do not expose raw participant data in the frontend;
-   keep research data separate from user-submission data;
-   do not upload private clinical information to GitHub.

If any real participant data is collected later, obtain
guide/institutional approval and follow the required consent/privacy
procedure.

------------------------------------------------------------------------

# 28. REPOSITORY STRUCTURE

Recommended repository:

``` text
adhd-screening-platform/
│
├── README.md
├── .gitignore
├── requirements.txt
├── LICENSE
│
├── data/
│   ├── README.md
│   ├── raw/
│   │   └── hyperaktiv/
│   ├── synthetic/
│   │   ├── README.md
│   │   └── synthetic_raw.csv
│   └── processed/
│       └── features.csv
│
├── pipeline/
│   ├── __init__.py
│   ├── batch_process.py
│   ├── preprocess.py
│   ├── feature_extraction.py
│   └── validation.py
│
├── model/
│   ├── __init__.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   └── artifacts/
│       └── .gitkeep
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── db/
│   └── routes/
│
├── frontend/
│   ├── index.html
│   ├── questionnaire.html
│   ├── attention.html
│   ├── gonogo.html
│   ├── results.html
│   ├── disclaimer.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── questionnaire.js
│       ├── attention.js
│       ├── gonogo.js
│       └── api.js
│
├── notebooks/
│   └── explore_dataset.ipynb
│
├── tests/
│   ├── test_preprocess.py
│   ├── test_features.py
│   ├── test_questionnaire.py
│   └── test_tasks.py
│
├── docs/
│   ├── architecture.md
│   ├── literature_review.md
│   └── research_notes.md
│
└── analytics_pipeline/
    └── (optional; implement only if approved)
```

Do not put large raw datasets, private participant data, model secrets,
or unnecessary generated files into GitHub.

------------------------------------------------------------------------

# 29. INITIAL 40% MILESTONE

The first major project checkpoint should demonstrate a meaningful
working foundation.

Target:

## Research

-   [x] Topic and problem defined
-   [x] Literature survey initiated/completed
-   [x] HYPERAKTIV dataset studied
-   [x] Research gap identified
-   [x] System architecture designed

## Data

-   [ ] HYPERAKTIV data organized
-   [ ] Dataset exploration notebook created
-   [ ] Synthetic data generator created
-   [ ] Synthetic dataset generated
-   [ ] Batch-processing pipeline implemented
-   [ ] Feature extraction implemented

## ML

-   [ ] Initial Random Forest experiment
-   [ ] Basic evaluation metrics
-   [ ] Confusion matrix

## Web

-   [ ] Flask project created
-   [ ] Homepage
-   [ ] Questionnaire prototype
-   [ ] Sustained Attention prototype
-   [ ] Basic SQLite storage

## Documentation

-   [ ] README
-   [ ] Architecture diagram
-   [ ] Dataset documentation
-   [ ] Git history with meaningful commits

This is enough to demonstrate substantial progress without pretending
that the final system is complete.

------------------------------------------------------------------------

# 30. IMPLEMENTATION ORDER

Claude Code should follow this order.

## Phase 0 --- Repository setup

1.  Create Git repository.
2.  Create project folders.
3.  Create virtual environment.
4.  Create `requirements.txt`.
5.  Create `.gitignore`.
6.  Create README.
7.  Make initial commit.

## Phase 1 --- Dataset exploration

1.  Locate HYPERAKTIV data.
2.  Document its structure.
3.  Load it with pandas.
4.  Inspect columns.
5.  Check missing values.
6.  Check class distribution.
7.  Identify usable variables.
8.  Create an exploratory notebook.
9.  Save findings in `docs/research_notes.md`.

## Phase 2 --- Synthetic dataset

1.  Define the schema.
2.  Build deterministic generator.
3.  Generate sample records.
4.  Validate ranges and missing values.
5.  Save to `data/synthetic/`.
6.  Document the synthetic-data assumptions.

## Phase 3 --- Batch pipeline

1.  Implement input loader.
2.  Implement schema validation.
3.  Implement cleaning.
4.  Implement feature extraction.
5.  Implement batch processing.
6.  Generate processed CSV.
7.  Add tests.

## Phase 4 --- ML baseline

1.  Load processed research data.
2.  Define target.
3.  Select candidate features.
4.  Avoid leakage.
5.  Build baseline.
6.  Train Random Forest.
7.  Evaluate.
8.  Save model artifact locally.
9.  Document metrics.

## Phase 5 --- Web foundation

1.  Create Flask application.
2.  Create homepage.
3.  Create disclaimer.
4.  Create questionnaire.
5.  Create attention task.
6.  Create Go/No-Go task.
7.  Store raw responses.
8.  Calculate task metrics.

## Phase 6 --- Integration

Only after the previous pieces are stable:

1.  Define application feature vector.
2.  Compare application features with ML training features.
3.  Decide whether direct model integration is scientifically valid.
4.  If valid, integrate.
5.  If not, clearly separate the research benchmark from the application
    behavioural-analysis prototype.
6.  Build results page.

## Phase 7 --- Testing and evaluation

1.  Unit tests.
2.  Data validation tests.
3.  Task timing tests.
4.  API tests.
5.  Database tests.
6.  End-to-end assessment test.
7.  ML evaluation.
8.  Error handling.
9.  UI usability check.

## Phase 8 --- Documentation

1.  Update README.
2.  Update architecture.
3.  Update methodology.
4.  Record limitations.
5.  Record experimental results.
6.  Update project diary.
7.  Prepare final presentation.

------------------------------------------------------------------------

# 31. GIT WORKFLOW

Use meaningful commits.

Examples:

``` text
chore: initialize project repository
docs: add project overview and research scope
docs: add system architecture
feat: add HYPERAKTIV exploration notebook
feat: add synthetic dataset generator
feat: add synthetic data validation
feat: implement batch preprocessing
feat: implement behavioural feature extraction
test: add feature extraction tests
feat: add Random Forest baseline
feat: create Flask application
feat: add questionnaire interface
feat: add sustained attention task
feat: add Go-No-Go task
feat: store cognitive trial data
feat: add results page
test: add end-to-end assessment tests
docs: update implementation progress
```

Never create meaningless commits such as:

``` text
update
changes
final
final2
done
```

Do not fabricate commit dates or hashes.

------------------------------------------------------------------------

# 32. BRANCHING / COLLABORATION

If the two team members work separately:

``` text
main
 ├── feature/backend
 ├── feature/frontend
 ├── feature/ml
 └── feature/dataset
```

Prefer small feature branches and pull requests.

Before merging:

-   code should run;
-   no secrets;
-   no private data;
-   README updated when needed;
-   tests should pass where applicable.

------------------------------------------------------------------------

# 33. CLAUDE CODE RULES

Claude Code should follow these rules throughout development.

## Rule 1 --- Do not redesign the project without approval

Do not suddenly replace:

-   Flask with Django;
-   SQLite with PostgreSQL;
-   classical ML with deep learning;
-   HTML/JS with React;
-   the dataset strategy;
-   the cognitive-task scope.

Ask before making major architectural changes.

## Rule 2 --- Prefer simple implementations

This is an MCA mini project with a short timeline.

Prefer:

``` text
simple + working + tested
```

over:

``` text
complex + impressive + unfinished
```

## Rule 3 --- Explain before large changes

Before generating a large number of files or changing the architecture,
explain:

-   what will be created;
-   why;
-   dependencies;
-   expected output;
-   how it fits the architecture.

Then proceed.

## Rule 4 --- Never invent research results

Do not invent:

-   participant counts;
-   accuracy;
-   clinical findings;
-   questionnaire validity;
-   model performance;
-   scientific conclusions.

If something has not been measured, label it:

> Planned

or:

> Not yet evaluated.

## Rule 5 --- Never treat synthetic data as real

Every synthetic dataset file must be labelled clearly.

## Rule 6 --- Do not expose sensitive data

Never commit:

-   real participant PII;
-   medical records;
-   credentials;
-   API keys;
-   `.env` secrets;
-   private datasets.

## Rule 7 --- Reproducibility

Use:

-   fixed random seeds where appropriate;
-   documented preprocessing;
-   deterministic feature extraction;
-   explicit requirements;
-   clear commands.

## Rule 8 --- Do not overfit the UI

The website is a research prototype.

Prioritize:

-   correct timing;
-   correct data capture;
-   correct storage;
-   correct feature extraction;
-   correct API behaviour.

Visual polish comes later.

## Rule 9 --- Test incrementally

After implementing a feature:

1.  run it;
2.  test it;
3.  inspect output;
4.  fix errors;
5.  commit.

Do not implement the entire project and test at the end.

------------------------------------------------------------------------

# 34. COMMANDS THE REPOSITORY SHOULD EVENTUALLY SUPPORT

The exact command names may be adjusted, but the project should aim for
a simple workflow.

Install:

``` bash
pip install -r requirements.txt
```

Generate synthetic data:

``` bash
python -m pipeline.generate_synthetic
```

Process data:

``` bash
python -m pipeline.batch_process
```

Train model:

``` bash
python -m model.train_model
```

Evaluate model:

``` bash
python -m model.evaluate_model
```

Run web application:

``` bash
python -m backend.app
```

Run tests:

``` bash
pytest
```

If module names differ, update README accordingly.

------------------------------------------------------------------------

# 35. EXPECTED FEATURE SET

Initial application feature vector can include:

## Questionnaire

``` text
questionnaire_score
```

## Sustained Attention

``` text
attention_accuracy
attention_mean_rt
attention_median_rt
attention_rt_std
attention_missed_targets
attention_false_responses
attention_false_response_rate
```

## Go/No-Go

``` text
gonogo_accuracy
gonogo_mean_rt
gonogo_median_rt
gonogo_rt_std
gonogo_false_alarms
gonogo_missed_go
gonogo_false_alarm_rate
```

The final feature set must be justified and should not be unnecessarily
large.

------------------------------------------------------------------------

# 36. RESULT PAGE DESIGN

A simple result page:

``` text
----------------------------------------
      Preliminary Screening Profile
----------------------------------------

Questionnaire
Score: XX

Sustained Attention
Accuracy: XX%
Average reaction time: XXX ms
Variability: XX

Go/No-Go
Accuracy: XX%
False alarms: XX

----------------------------------------
Overall Screening-Oriented Profile
----------------------------------------

[Profile / indicator]

----------------------------------------
IMPORTANT
This result is for research and preliminary
screening purposes only. It is not a medical
diagnosis and should not replace professional
clinical assessment.
----------------------------------------
```

Use charts only where they make interpretation easier.

------------------------------------------------------------------------

# 37. TESTING STRATEGY

Testing must cover four levels.

## Unit tests

Examples:

-   feature calculations;
-   questionnaire scoring;
-   preprocessing;
-   validation;
-   model input shape.

## Data tests

Check:

-   required columns;
-   valid ranges;
-   missing values;
-   duplicate records;
-   label consistency.

## Browser task tests

Check:

-   instructions appear;
-   trials execute;
-   responses are recorded;
-   timestamps are recorded;
-   reaction times are non-negative;
-   correct/incorrect classification works;
-   task completion works.

## Integration tests

Example:

``` text
Complete questionnaire
        ↓
Complete attention test
        ↓
Complete Go/No-Go
        ↓
Submit
        ↓
Backend receives data
        ↓
Database stores data
        ↓
Features calculated
        ↓
Results page loads
```

------------------------------------------------------------------------

# 38. RESEARCH EVALUATION

The final research evaluation should answer:

1.  Does the data pipeline process the research dataset correctly?
2.  Which features are useful?
3.  How does Random Forest perform?
4.  How does it compare with a baseline?
5.  Are results stable under cross-validation?
6.  Are there signs of class imbalance?
7.  Are there data-leakage risks?
8.  What are the limitations of the dataset?
9.  Can application-generated features be mapped validly to the research
    model?
10. What cannot be concluded from the experiment?

The project should value honest limitations.

------------------------------------------------------------------------

# 39. EXPECTED LIMITATIONS

The final report should explicitly discuss:

-   small number of participants in HYPERAKTIV;
-   dataset-specific findings;
-   possible class/distribution limitations;
-   incomplete heart-rate coverage;
-   difference between research-dataset features and browser-generated
    features;
-   absence of a large independent validation population;
-   synthetic data being unsuitable as clinical evidence;
-   browser hardware/software timing variability;
-   screening versus diagnosis;
-   potential demographic/generalisation limitations.

------------------------------------------------------------------------

# 40. IMPORTANT SCIENTIFIC INTEGRATION ISSUE

This is a key open question.

The original concept says:

``` text
Browser cognitive task
       ↓
Behavioural features
       ↓
Random Forest trained on HYPERAKTIV
       ↓
Risk prediction
```

But this is only scientifically valid if the training features and
application features are compatible.

For example:

``` text
HYPERAKTIV model features:
activity + heart rate + CPT-II
```

are different from:

``` text
Browser features:
attention accuracy + reaction time + false alarms
```

Therefore the implementation must first inspect the actual dataset and
determine whether:

### Option A

The HYPERAKTIV data contains suitable behavioural/task variables that
can be transformed into features comparable to the browser tasks.

### Option B

The research ML model and browser behavioural model should remain
separate research components.

### Option C

A new compatible dataset/experimental design can be established with
guide approval.

**Do not force an invalid mapping just to make the architecture look
complete.**

This issue should be discussed with the project guide before final
ML-to-website integration.

------------------------------------------------------------------------

# 41. INTERIM PRESENTATION DEMO

At the interim stage, the best demo is not the final product.

Show:

``` text
1. GitHub repository
        ↓
2. Dataset exploration
        ↓
3. Synthetic dataset
        ↓
4. Batch-processing pipeline
        ↓
5. Processed feature CSV
        ↓
6. Initial ML experiment
        ↓
7. Questionnaire prototype
        ↓
8. Cognitive-task prototype
```

A working partial system is preferable to a fake finished system.

------------------------------------------------------------------------

# 42. WHAT COUNTS AS APPROXIMATELY 40% COMPLETE

A practical 40% milestone is:

### Completed

-   project repository;
-   README;
-   architecture;
-   dataset exploration;
-   HYPERAKTIV understanding;
-   synthetic dataset generator;
-   synthetic dataset;
-   batch-processing pipeline;
-   feature extraction;
-   initial ML experiment;
-   Flask foundation;
-   questionnaire prototype;
-   one cognitive task;
-   basic tests;
-   meaningful Git history.

### Not yet required

-   N-Back;
-   NLP;
-   complete dashboard;
-   final model integration;
-   deployment;
-   large participant study;
-   polished UI;
-   final research conclusions.

------------------------------------------------------------------------

# 43. FINAL DEVELOPMENT TARGET

The final system should ideally look like:

``` text
                         USER
                           │
                           ▼
                    Consent / Disclaimer
                           │
                           ▼
                     Questionnaire
                           │
                           ▼
                  Cognitive Assessment
                     /           \
                    /             \
                   ▼               ▼
            Sustained Attention  Go/No-Go
                    │               │
                    └───────┬───────┘
                            ▼
                    Behavioural Data
                            │
                            ▼
                     Feature Engine
                            │
                            ▼
                    Validated Analysis
                            │
                            ▼
                 Preliminary Screening
                         Profile
                            │
                            ▼
                      Result Dashboard
```

In parallel:

``` text
HYPERAKTIV
    ↓
Research preprocessing
    ↓
Feature engineering
    ↓
ML experiments
    ↓
Evaluation
```

And during development:

``` text
Synthetic dataset
    ↓
Pipeline validation
    ↓
Software testing
```

------------------------------------------------------------------------

# 44. DEFINITION OF DONE

A module is not considered complete merely because code exists.

A module is complete when:

-   code runs;
-   expected output is produced;
-   basic errors are handled;
-   at least relevant tests exist;
-   README/documentation is updated where necessary;
-   Git commit is made;
-   no sensitive data/secrets are committed.

The complete project is done when:

-   research pipeline is reproducible;
-   application workflow is functional;
-   cognitive tasks collect reliable structured data;
-   ML experiments are documented;
-   integration is scientifically justified;
-   tests pass;
-   limitations are documented;
-   project diary and Git history reflect actual work;
-   final presentation/report are consistent with the implementation.

------------------------------------------------------------------------

# 45. REFERENCES / SOURCE DOCUMENTS

The current project understanding is based on the team's uploaded
project document and the project diary/template.

Important research references currently identified in the project
documentation include:

1.  Hicks, S. A., Stautland, A., Fasmer, O. B., et al. (2021).
    "HYPERAKTIV: An Activity Dataset from Adult Patients with
    Attention-Deficit/Hyperactivity Disorder (ADHD)." Proceedings of the
    12th ACM Multimedia Systems Conference (MMSys '21), pp. 314--319.
2.  Kessler, R. C., et al. (2005). WHO Adult ADHD Self-Report Scale
    (ASRS).
3.  A machine-learning-based investigation of ADHD diagnosis using the
    HYPERAKTIV dataset.
4.  Accurate identification of ADHD among adults using real-time
    activity data.
5.  O'Mahony et al. (2014), objective ADHD diagnosis using inertial
    measurement units.
6.  Relevant NLP-based ADHD textual-data research.
7.  scikit-learn documentation.
8.  Flask documentation.
9.  spaCy documentation.
10. Chart.js documentation.

The exact bibliographic details must be verified before final
submission.

------------------------------------------------------------------------

# 46. INSTRUCTIONS FOR THE AI CODING AGENT

When this document is loaded into an AI coding agent, the agent should
behave as a **technical implementation assistant**, not as an autonomous
research-direction changer.

Before starting:

1.  Inspect the repository.
2.  Compare the existing files against this specification.
3.  Identify what is already implemented.
4.  Do not overwrite working code unnecessarily.
5.  Create a short implementation plan.
6.  Start with the highest-priority incomplete module.

For every significant feature:

``` text
Understand
   ↓
Plan
   ↓
Implement
   ↓
Run
   ↓
Test
   ↓
Review
   ↓
Commit
```

When uncertain about scientific validity, do not invent an answer. Flag
the issue for the project team/guide.

When uncertain about an optional feature, prefer leaving it out until
the core project is stable.

------------------------------------------------------------------------

# 47. CURRENT PRIORITY ORDER

If development time becomes limited, prioritize in exactly this order:

``` text
1. Data understanding
2. Reproducible preprocessing
3. Feature extraction
4. Synthetic-data pipeline
5. Initial ML experiment
6. Questionnaire
7. Sustained Attention
8. Go/No-Go
9. Flask integration
10. SQLite persistence
11. Results page
12. Testing
13. Documentation
14. N-Back
15. NLP insights
16. UI polish
17. Deployment
```

The project should be considered successful if the first 13 items are
implemented well.

------------------------------------------------------------------------

# 48. ONE-SENTENCE PROJECT SUMMARY

> **This project investigates a lightweight browser-based approach for
> preliminary ADHD risk screening by combining questionnaire responses
> and behavioural measurements from short cognitive tasks with
> reproducible data-processing and machine-learning experimentation
> using the HYPERAKTIV research dataset, while using synthetic data only
> for development and pipeline validation.**

------------------------------------------------------------------------

# 49. FINAL PRINCIPLE

The goal is **not** to build the most complicated ADHD AI system
possible.

The goal is to build a:

> **small, reproducible, technically working, research-oriented and
> scientifically honest system**

within the available time.

The implementation should therefore favour:

**correctness \> complexity**

**reproducibility \> impressive claims**

**working modules \> unfinished features**

**measured results \> invented results**

**clear research limitations \> exaggerated conclusions**
