# ADHD Insight --- Website Building Specification

## 1. Project Overview

**Application:** Research-oriented behavioural assessment web
application\
**Backend:** Python + Flask\
**Database:** SQLite + SQLAlchemy\
**Frontend:** HTML5 + CSS3 + JavaScript\
**Charts:** Chart.js\
**Data processing:** Pandas + NumPy\
**ML:** Scikit-learn, integrated only after feature compatibility is
scientifically verified

The website is a prototype for an academic research project. It combines
a questionnaire, browser-based cognitive tasks, raw behavioural event
collection, feature extraction, analysis/machine-learning
experimentation, and a non-diagnostic behavioural profile.

**The system must not claim to diagnose ADHD.**

------------------------------------------------------------------------

## 2. Core User Workflow

``` text
Home
  ↓
Consent & Disclaimer
  ↓
Start Assessment
  ↓
Questionnaire
  ↓
Sustained Attention Test
  ↓
Go/No-Go Test
  ↓
Processing
  ↓
Results Dashboard
```

A separate **About / Research** page explains the methodology.

Main navigation:

-   Home
-   About
-   Start Assessment

During an assessment, use a controlled step-by-step flow.

------------------------------------------------------------------------

## 3. Recommended Pages

  -----------------------------------------------------------------------
  Page                    Purpose                 Priority
  ----------------------- ----------------------- -----------------------
  Home                    Introduce platform and  Essential
                          start assessment        

  Consent                 Explain purpose,        Essential
                          privacy and limitations 

  Questionnaire           Collect self-reported   Essential
                          responses               

  Sustained Attention     Measure                 Essential
                          attention-related       
                          behavioural features    

  Go/No-Go                Measure response        Essential
                          inhibition              

  Processing              Show analysis progress  Recommended

  Results                 Display behavioural     Essential
                          profile                 

  About / Research        Explain methodology and Recommended
                          research context        
  -----------------------------------------------------------------------

Do not build login, registration, doctor portal, admin portal, payment,
chatbot, or other non-essential features during the first version.

------------------------------------------------------------------------

## 4. UI / Visual Theme

### Design direction

Use a modern research/health-tech interface that feels:

-   Clean
-   Calm
-   Scientific
-   Modern
-   Accessible
-   Trustworthy
-   Minimal

Avoid making it look like a generic hospital website or a flashy AI
landing page.

Avoid phrases such as:

-   AI Diagnosis
-   Diagnose ADHD
-   You have ADHD

Prefer:

-   Behavioural Assessment
-   Screening-Oriented Analysis
-   Behavioural Profile
-   Research Assessment
-   Preliminary Screening Indication

### Suggested palette

``` text
Primary Purple  #6C3EF4
Blue            #4A90E2
Mint            #00B894
Orange          #F5A623
Red             #FF6666
Dark Text       #182033
Muted Text      #687280
Light Background#F7F8FC
```

These are design suggestions; keep the system consistent.

### Typography

Recommended:

-   Poppins for headings
-   Inter for body/UI

Suggested hierarchy:

-   Main heading: 36--48px
-   Section heading: 24--32px
-   Card heading: 18--22px
-   Body: 15--17px
-   Supporting text: 13--14px

------------------------------------------------------------------------

## 5. Reusable UI Components

Create reusable components rather than styling every page independently.

Recommended:

-   Navbar
-   Footer
-   Primary button
-   Secondary button
-   Card
-   Progress indicator
-   Assessment stepper
-   Radio option
-   Checkbox
-   Metric card
-   Progress bar
-   Alert/disclaimer
-   Loading indicator
-   Chart container
-   Result status card

Use `templates/base.html` as the shared template.

------------------------------------------------------------------------

# 6. Home Page

The home page should explain the project simply and lead the user into
the assessment.

Suggested hero:

``` text
Understand
Your Behavioural
Patterns

A research-oriented platform that combines
questionnaire responses and cognitive tasks
to generate behavioural insights.

[ Begin Assessment ]

Scientific Approach
Research Based
Privacy Focused

Research prototype • Non-diagnostic
```

Possible supporting cards:

``` text
Questionnaire | Cognitive Tasks | Insights & Analysis
```

------------------------------------------------------------------------

# 7. Consent Page

Explain:

### Purpose

Why the assessment exists.

### What happens

``` text
Questionnaire
      ↓
Attention Task
      ↓
Go/No-Go Task
      ↓
Behavioural Analysis
```

Include a clear disclaimer:

> This platform is developed for academic research and preliminary
> screening research. It does not provide a medical diagnosis and should
> not replace assessment by a qualified healthcare professional.

Add:

``` text
☐ I understand the above information.

[ Continue ]
```

Disable Continue until consent is given.

------------------------------------------------------------------------

# 8. Assessment Progress Indicator

Use a consistent stepper:

``` text
✓ Consent
   ↓
● Questionnaire
   ↓
○ Attention
   ↓
○ Go/No-Go
   ↓
○ Results
```

The current step should be highlighted.

------------------------------------------------------------------------

# 9. Questionnaire Page

Use one question at a time.

Example:

``` text
Question 3 of 6

How often do you have difficulty
keeping your attention when doing
something boring or repetitive?

○ Never
○ Rarely
○ Sometimes
○ Often
○ Very Often

[ Previous ]                 [ Next ]

██████████░░░░░░ 50%
```

Required:

-   Validation
-   Previous/Next
-   Progress indicator
-   Final submission
-   Score calculation
-   Session association

Store individual responses, not just the final score.

------------------------------------------------------------------------

# 10. Sustained Attention Test

Instruction screen:

``` text
SUSTAINED ATTENTION TEST

You will see a series of stimuli.

Press SPACE when you see the target.

Try to respond as quickly and accurately
as possible.

[ Start Test ]
```

Testing screen:

``` text
--------------------------------------
|                                    |
|                  X                 |
|                                    |
|                                    |
|             Trial 23 / 50          |
--------------------------------------
```

Keep the actual task simple and distraction-free.

### Raw trial data

Example:

``` json
{
  "trial": 23,
  "stimulus": "X",
  "expected_response": true,
  "actual_response": true,
  "reaction_time_ms": 421,
  "correct": true,
  "timestamp": "..."
}
```

Potential derived features:

-   Accuracy
-   Mean reaction time
-   Median reaction time
-   Reaction-time standard deviation
-   Reaction-time coefficient of variation
-   Missed targets
-   False responses
-   Response consistency

Only use features supported by the final research design.

------------------------------------------------------------------------

# 11. Go/No-Go Test

Instruction:

``` text
GO / NO-GO TEST

Press SPACE when you see GREEN.

Do NOT press anything when you see RED.

Try to respond accurately.

[ Start Test ]
```

Testing screen:

``` text
--------------------------------------
|                                    |
|                  ●                 |
|                                    |
|             Trial 17 / 40          |
--------------------------------------
```

Potential features:

-   Accuracy
-   Mean reaction time
-   Reaction-time variability
-   False alarms
-   Missed go trials
-   Inhibition-related error rate

------------------------------------------------------------------------

# 12. Processing Page

After all tasks:

``` text
Assessment Complete

✓ Questionnaire
✓ Attention Test
✓ Go/No-Go Test

● Extracting Behavioural Features
○ Generating Report

Analyzing data...

████████████░░░ 70%
```

The UI should communicate progress without pretending that a long
computation is happening if processing is actually instantaneous.

------------------------------------------------------------------------

# 13. Results Dashboard

Do not display a simplistic `ADHD: YES`.

Show a behavioural profile.

Example:

``` text
YOUR BEHAVIOURAL PROFILE

Assessment completed on 30 Aug 2026

Questionnaire
28 / 54
Moderate

Sustained Attention
Accuracy             86%
Mean Reaction Time   421 ms
RT Variability       73 ms

Go / No-Go
Accuracy             91%
False Alarms         4
Mean Reaction Time   398 ms

OVERALL SCREENING INDICATION

Moderate Indication

This result is generated for academic research
and preliminary screening only.

It is NOT a medical diagnosis.
```

### Recommended charts

Keep the dashboard simple.

1.  Attention reaction-time line chart
2.  Attention vs Go/No-Go accuracy bar chart
3.  Metric cards for RT, RT variability, false alarms, accuracy

Chart.js is sufficient.

------------------------------------------------------------------------

# 14. About / Research Page

Suggested sections:

### About the Project

Academic purpose.

### Research Objective

What the project investigates.

### Methodology

``` text
Questionnaire
      +
Cognitive Tasks
      ↓
Behavioural Features
      ↓
Analysis / ML
      ↓
Behavioural Profile
```

### Dataset & Research

Explain the role of HYPERAKTIV and other research data according to the
approved methodology.

**Important:** Do not assume that website-generated features are
interchangeable with HYPERAKTIV features. Verify feature compatibility
experimentally and scientifically first.

### Technology

-   Python
-   Flask
-   JavaScript
-   SQLite
-   SQLAlchemy
-   Pandas
-   NumPy
-   Scikit-learn
-   Chart.js

------------------------------------------------------------------------

# 15. Database Design

Use SQLite for the prototype and SQLAlchemy as ORM.

## `assessment_sessions`

``` text
id
session_id
started_at
completed_at
status
```

Statuses:

-   `in_progress`
-   `completed`
-   `abandoned`

Avoid unnecessary personal identifiers.

## `questionnaire_responses`

``` text
id
session_id
question_id
response
created_at
```

## `cognitive_trials`

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

Store raw behavioural events.

## `assessment_results`

``` text
id
session_id

questionnaire_score

attention_accuracy
attention_mean_rt
attention_rt_std
attention_missed
attention_false_responses

gonogo_accuracy
gonogo_mean_rt
gonogo_rt_std
gonogo_false_alarms

screening_indicator

created_at
```

Store derived results separately from raw events.

### Relationship

``` text
assessment_sessions
        │
        ├── questionnaire_responses
        │
        └── cognitive_trials
                  │
                  ▼
          feature extraction
                  │
                  ▼
          assessment_results
```

------------------------------------------------------------------------

# 16. Anonymous Session Architecture

Do not implement login/signup initially.

When Start Assessment is clicked, generate an anonymous session ID.

Example:

``` text
ASMT-7F3A91
```

All data is associated with that ID:

``` text
ASMT-7F3A91
    ├── questionnaire responses
    ├── attention trials
    ├── Go/No-Go trials
    └── assessment results
```

------------------------------------------------------------------------

# 17. Flask API Structure

Suggested endpoints:

``` text
POST /api/session/start
POST /api/questionnaire
POST /api/cognitive/attention
POST /api/cognitive/gonogo
GET  /api/results/<session_id>
```

Optional:

``` text
POST /api/session/complete
```

Architecture:

``` text
Browser JavaScript
       │ JSON
       ▼
Flask API
       │
       ▼
SQLAlchemy
       │
       ▼
SQLite
```

------------------------------------------------------------------------

# 18. Recommended Project Structure

``` text
ADHD-Insight/
│
├── app.py
├── config.py
├── extensions.py
│
├── models/
│   ├── __init__.py
│   ├── session.py
│   ├── questionnaire.py
│   ├── cognitive.py
│   └── result.py
│
├── routes/
│   ├── __init__.py
│   ├── main.py
│   ├── assessment.py
│   ├── questionnaire.py
│   ├── cognitive.py
│   └── results.py
│
├── services/
│   ├── scoring.py
│   ├── feature_extraction.py
│   └── analysis.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── consent.html
│   ├── questionnaire.html
│   ├── attention.html
│   ├── gonogo.html
│   ├── processing.html
│   ├── results.html
│   └── about.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── questionnaire.js
│   │   ├── attention.js
│   │   ├── gonogo.js
│   │   └── results.js
│   └── images/
│
├── data/
│   └── README.md
│
├── ml/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── models/
│   └── evaluation/
│
├── tests/
│
├── requirements.txt
├── README.md
└── PROJECT_SPECIFICATION.md
```

------------------------------------------------------------------------

# 19. Website vs ML Pipeline

Keep the website and ML research code separate.

``` text
Website
   │
   ├── collects data
   └── stores data
           │
           ▼
      Feature Layer
           │
           ▼
       ML Research
```

The ML pipeline should be independently reproducible.

------------------------------------------------------------------------

# 20. Critical ML Constraint

Do not automatically connect a model trained on HYPERAKTIV to browser
features.

Investigate:

1.  Which features exist in HYPERAKTIV?
2.  Which features are generated by the website?
3.  Whether the same constructs are being measured
4.  Whether feature distributions are compatible
5.  Whether a common feature representation is justified
6.  Whether a separate model should be trained
7.  Whether deployment would be scientifically valid

If compatibility cannot be demonstrated, keep:

``` text
Website behavioural analysis
```

and

``` text
HYPERAKTIV ML experiment
```

as related but separate research components.

Never create a scientifically invalid model connection just to make the
demo work.

------------------------------------------------------------------------

# 21. Privacy

Because this project concerns behavioural and mental-health-related
assessment:

-   Minimize personal information
-   Prefer anonymous session IDs
-   Do not collect names unless required
-   Do not collect emails unless required
-   Explain the research purpose
-   Explain limitations
-   Never present results as a medical diagnosis
-   Prevent one participant from accessing another participant's data
-   Keep raw data and derived results logically separated

Document these decisions in the README/report.

------------------------------------------------------------------------

# 22. Accessibility and Responsive Design

Support:

-   Desktop
-   Laptop
-   Tablet
-   Mobile

Implement:

-   Semantic HTML
-   Keyboard navigation
-   Visible focus states
-   Proper labels
-   Good contrast
-   Clear validation messages
-   Large clickable controls
-   Do not rely only on colour

For timed cognitive tasks, document accessibility limitations because
keyboard and reaction-time requirements may affect participation.

------------------------------------------------------------------------

# 23. Error Handling

Handle:

-   Missing questionnaire responses
-   Invalid session IDs
-   Duplicate submissions
-   Interrupted assessments
-   Database failures
-   Empty cognitive trial data
-   Invalid reaction times
-   Network failure

User-facing errors should be clear:

``` text
Something went wrong while saving your response.

Please try again.
```

Never expose Python stack traces to users.

------------------------------------------------------------------------

# 24. Development Milestones

## Milestone 1 --- Flask Foundation

Build:

-   Flask app
-   Base template
-   Navbar
-   Home
-   About
-   Static CSS/JS

## Milestone 2 --- Assessment Session

Build:

-   Consent
-   Anonymous session generation
-   Session state
-   Database connection

## Milestone 3 --- Questionnaire

Build:

-   Questions
-   One-question-at-a-time UI
-   Validation
-   Progress indicator
-   Database storage
-   Scoring

## Milestone 4 --- Sustained Attention

Build:

-   Instruction screen
-   Trial engine
-   Keyboard event capture
-   Reaction time
-   Accuracy
-   Raw trial storage

## Milestone 5 --- Go/No-Go

Build:

-   Instructions
-   Stimulus presentation
-   Response capture
-   Reaction time
-   Error classification
-   Raw storage

## Milestone 6 --- Feature Extraction

``` text
Raw trials
    ↓
Cleaning
    ↓
Feature calculation
    ↓
Feature vector
```

## Milestone 7 --- Results Dashboard

Build:

-   Metric cards
-   Charts
-   Behavioural profile
-   Disclaimer
-   Optional report export

## Milestone 8 --- ML Research

Only after feature compatibility is established:

``` text
Dataset
→ preprocessing
→ feature engineering
→ train/test split
→ model
→ evaluation
→ comparison
```

Possible models:

-   Logistic Regression
-   Random Forest
-   SVM
-   Gradient Boosting

Report appropriate metrics such as:

-   Accuracy
-   Precision
-   Recall
-   F1-score
-   Confusion matrix
-   ROC-AUC where appropriate

Do not optimize solely for accuracy.

------------------------------------------------------------------------

# 25. Recommended Build Order for a Tight Deadline

Build a working version early:

``` text
Home
  ↓
Consent
  ↓
Questionnaire
  ↓
Attention Test
  ↓
Results
```

Then add:

``` text
Go/No-Go
```

Then:

``` text
Feature Extraction
```

Then:

``` text
ML research integration
```

This provides a demonstrable prototype before the entire project is
complete.

------------------------------------------------------------------------

# 26. 40% GitHub Milestone

A credible \~40% milestone should include:

### Website

-   Flask application running
-   Home page
-   Consent page
-   Questionnaire page
-   Base UI theme
-   Navigation
-   Responsive styling

### Backend

-   SQLite database
-   SQLAlchemy models
-   Session creation
-   Questionnaire storage

### Cognitive module

At least:

-   Sustained Attention prototype
-   Trial generation
-   Keyboard event capture
-   Reaction-time calculation
-   Raw trial storage

### Research code

-   Initial dataset structure
-   Preprocessing scripts
-   Initial feature extraction
-   Initial exploratory analysis

### Documentation

-   README
-   Project specification
-   Architecture diagram
-   Database design
-   Setup instructions

------------------------------------------------------------------------

# 27. GitHub Commit Strategy

Use meaningful commits:

``` text
chore: initialize Flask project
feat: add base UI theme
feat: add assessment session management
feat: implement consent page
feat: implement questionnaire workflow
feat: store questionnaire responses
feat: implement sustained attention task
feat: store cognitive trial data
feat: add feature extraction pipeline
docs: add project architecture
docs: update README
test: add questionnaire scoring tests
```

Avoid one huge final commit.

------------------------------------------------------------------------

# 28. Instructions for Claude Code

Before modifying the repository, Claude Code should:

1.  Read this entire file.
2.  Inspect the existing repository.
3.  Identify what is already implemented.
4.  Compare the repository against this specification.
5.  Report missing components.
6.  Identify scientific or architectural inconsistencies.
7.  Propose the next smallest implementation step.
8.  Ask before changing project scope.

Do not ask Claude to generate the whole project in one step.

Recommended first prompt:

> Read `WEBSITE_BUILDING_SPECIFICATION.md` completely and inspect the
> repository. Do not modify anything yet. Tell me the current project
> state, what is missing, and the smallest next implementation step.

Then implement one milestone at a time.

------------------------------------------------------------------------

# 29. Definition of Done

A functional prototype should support:

``` text
User
 ↓
Starts anonymous session
 ↓
Provides consent
 ↓
Completes questionnaire
 ↓
Completes attention task
 ↓
Completes Go/No-Go
 ↓
Raw data stored
 ↓
Features extracted
 ↓
Results calculated
 ↓
Behavioural profile displayed
```

The ML component is complete only when training, validation, evaluation,
and deployment are scientifically justified and reproducible.

------------------------------------------------------------------------

# 30. Final Product Vision

> **ADHD Insight is a research-oriented behavioural assessment platform
> that combines self-reported questionnaire responses with browser-based
> cognitive task measurements to investigate behavioural patterns
> related to attention and response inhibition.**

The website is the **data collection and user-facing layer**.

The research pipeline is the **analysis and machine-learning layer**.

``` text
             ADHD INSIGHT
                  │
       ┌──────────┴──────────┐
       ▼                     ▼
   Web Platform          ML Research
       │                     │
 Questionnaire         Research Dataset
       │                     │
 Cognitive Tasks       Preprocessing
       │                     │
 Raw Behavioural Data  Feature Engineering
       │                     │
       └──────────┬──────────┘
                  ▼
          Behavioural Analysis
                  │
                  ▼
          Screening-Oriented
             Profile
```

**Central principle:** Build a reliable data-collection and
behavioural-analysis prototype first. Add machine learning only where
the available data and feature representation support it scientifically.
