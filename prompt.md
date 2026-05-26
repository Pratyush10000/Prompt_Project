# Context and Role

Act as a Senior Full-Stack Machine Learning Engineer, Explainable AI Researcher, and Enterprise Software Architect. The role includes creating a production-level mental health awareness platform that uses Explainable AI technology.

The system needs to assess emotional distress levels through PHQ-9 questionnaire responses, and it should produce continuous PHQ score predictions through regression analysis, generate SHAP-based explanations that humans can understand, and produce PDF reports for download while showing results through a user interface that promotes relaxation, support, and accessibility.

The application needs to follow clean architecture principles while developers build it through modular development and scalable engineering standards, which support ethical communication and produce maintainable software that works in production environments.

# Objective

- Predict a continuous PHQ-9 score using machine learning regression.
- Map predicted scores into mental health severity levels.
- Generate SHAP-based explainability for each prediction.
- Convert technical explanations into emotionally safe, human-readable insights.
- Provide supportive recommendations based on influencing factors.
- Include a modern, responsive frontend interface.
- Generate downloadable PDF assessment reports.
- Maintain a secure, modular, and scalable backend architecture.
- Use the user-provided dataset at `data/phq9.csv` for all training and inference.
- Do not use synthetic data under any circumstances.

# Important Domain and Ethical Requirements

## Mental Health Safety Rules

The platform must:

- Function strictly as an educational and awareness tool.
- Never claim to provide a medical diagnosis.
- Avoid alarming, judgmental, or harmful wording.
- Use supportive, empathetic, and calm language throughout the UI and reports.
- Present explanations in simple human-readable language instead of technical jargon.
- Present confidence values as calibrated estimates only.
- Include clear disclaimers wherever predictions are shown.

## Communication Standards

The system must ensure:

- Emotionally safe messaging.
- Non-clinical phrasing.
- Clear explanation readability.
- Ethical AI communication principles.
- Responsible prediction presentation.

# Dataset and Data Processing Requirements

## Dataset Usage

The system must:

- Use the real dataset CSV file provided by the user, located at `data/phq9.csv`.
- Infer schema and feature columns dynamically from the dataset.
- Avoid inventing synthetic columns unless explicitly instructed.
- Validate dataset consistency before training.
- Ensure strict feature alignment between training and inference — the same features in the same order.

## Data Preprocessing

Implement preprocessing pipelines that:

- Handle missing values appropriately.
- The imputation strategy used must be documented in code comments.
- Support categorical encoding (e.g., one-hot or ordinal as appropriate per column).
- Support numeric feature scaling if necessary.
- Prevent data leakage — all transformations must be fit only on training data, never on the full dataset.
- Maintain identical preprocessing during inference as during training.

## Validation Requirements

Include:

- Implement a proper train/test split strategy (e.g., 80/20).
- Model evaluation metrics:
  - MAE
  - RMSE
  - R²
- Cross-validation if the dataset size warrants it.
- Proper schema validation checks before training and before inference.

The system must not:

- Create fabricated dataset statistics.
- Invent evaluation metrics.
- Claim unsupported model performance.

# Machine Learning Requirements

## Model Objectives

Build a regression-based machine learning pipeline that:

- Predicts a continuous PHQ score.
- Uses Explainable AI techniques for interpretability.
- Supports reliable inference and scalable deployment.

## Severity Mapping

| Severity Level | PHQ Score Range |
| --- | --- |
| Minimal | 0–4 |
| Mild | 5–9 |
| Moderate | 10–14 |
| Moderately Severe | 15–19 |
| Severe | 20–27 |

## Model Persistence

The system should save and cleanly load at startup:

- `model/phq9_pipeline.pkl` — trained preprocessing and model pipeline.
- `model/shap_explainer.pkl` — fitted SHAP explainer.
  - Use `shap.TreeExplainer` for XGBoost.
  - Fall back to `shap.KernelExplainer` only if necessary, with a documented reason.
- `model/feature_names.json` — ordered list of feature names used during training.

All artifacts must load at Flask startup without requiring retraining.

# Explainability Requirements

## SHAP Integration

Use SHAP to:

- Discover influential features per prediction.
- Rank influential features by SHAP contribution magnitude.
- Make prediction behavior understandable.

## Human-Readable Explanations

The explainability system must:

- Convert SHAP outputs into insights that are easy to understand.
- Use simple, emotionally safe language when explaining predictions to end users.
- Avoid technical AI terminology.
- Generate explanations that are supportive and considerate of users' feelings.
- Be careful not to make things sound more certain than they really are.

### Example of Required Transformation

#### Wrong

```text
Feature 'sleep_quality' has a SHAP value of -1.43.
```

#### Correct

```text
Sleep quality appeared to be a notable factor in your results. Difficulty sleeping can sometimes affect how we feel overall.
```

## Suggestion Generation

Generate supportive recommendations based on:

- Major contributing factors.
- Severity level.
- Behavioral indicators.

Suggestions should remain:

- Supportive
- Ethical
- Calm
- Non-diagnostic

# Backend Requirements

## Framework Requirements

Use:

- Flask
- Python
- Gunicorn

## API Requirements

### 1. Home Route

| Property | Value |
| --- | --- |
| Route | `/` |
| Method | `GET` |
| Purpose | Renders the home page of the application. |

### 2. Prediction Route

| Property | Value |
| --- | --- |
| Route | `/predict` |
| Method | `POST` |
| Purpose | Accepts user input payload and returns the prediction result in JSON format along with explanations. |

### 3. Report Generation Route

| Property | Value |
| --- | --- |
| Route | `/report` |
| Method | `POST` |
| Purpose | Accepts the prediction result and generates a downloadable PDF report. |

### 4. Health Check Route

| Property | Value |
| --- | --- |
| Route | `/health` |
| Method | `GET` |
| Purpose | Returns the system health status and confirms whether the ML model is loaded successfully. |

## Backend Functionality

The backend should:

- Dynamically load trained models.
- Load SHAP explainers efficiently during runtime initialization.
- Validate incoming payloads.
- Predict PHQ scores.
- Generate severity levels.
- Produce explanations and suggestions.
- Return structured JSON responses.

## Input Payload Schema

The `/predict` endpoint expects the following fields at minimum. Additional fields are inferred dynamically from the dataset schema.

```json
{
  "age": "integer, required, range 10–100",
  "gender": "string, required, one of [Male, Female, Other]",
  "sleep_quality": "integer, required, range 1–5",
  "study_pressure": "integer, required, range 1–5",
  "financial_pressure": "integer, required, range 1–5"
}
```

## Security and Validation Requirements

Implement:

- Type and range validation on all inputs before inference.
- Structured JSON error responses with appropriate HTTP status codes.
- Safe parsing and validation of incoming requests.
- Secure environment variable handling for configuration management.
- Secure configuration management practices.

# Frontend Requirements

## UI Design Requirements

Plan a clean, responsive healthcare-oriented UI with the following features:

- PHQ-9 questionnaire form
- Registered age input
- Gender input
- Sleep quality input
- Study pressure input
- Financial pressure input

## Result Display Requirements

Display:

- Estimated PHQ Score
- Severity level
- Confidence level
  - Clearly labeled as a calibrated estimate, not a certainty
- Severity category visualization
- Confidence visualization bar
- Explanation table in plain, non-technical language
- Supportive recommendations
- Medical disclaimer
  - Always visible near results
  - Never hidden

## User Experience Requirements

The frontend should:

- Be mobile-optimized.
- Use accessible labels and fonts.
- Allow asynchronous form submission using fetch.
- Display loading states gracefully.
- Provide clear validation feedback for incomplete or invalid form inputs.
- Avoid page refreshes.
- Present results in a calm and understandable way.

## Animation and Interaction Requirements

Include:

- Smooth transitions
- User-friendly UI
- Distraction-free animations
- Performance-friendly rendering

# PDF Reporting Requirements

## Generate Downloadable PDF Reports Containing

- Date of assessment
- PHQ score
- Level of severity
- Confidence prediction
- Summary of risks
- Key contributing factors affecting the prediction
- Support recommendations
- Medical disclaimer

## PDF Design Requirements

Reports should be:

- Printable
- Structured
- Professional
- Easy to read

Use:

- ReportLab

# Architecture Requirements

## Project Structure

```text
phq9-xai-platform/
├── app/
│   ├── __init__.py              # Application factory
│   ├── app.py                   # Entry point
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── predict.py           # /predict route
│   │   └── report.py            # /report route
│   ├── services/
│   │   ├── model_loader.py      # Load pipeline and SHAP explainer
│   │   ├── predictor.py         # Run inference
│   │   ├── explainer.py         # SHAP to plain language
│   │   ├── suggester.py         # Recommendation logic
│   │   └── pdf_generator.py     # ReportLab report
│   ├── utils/
│   │   ├── validators.py        # Payload validation
│   │   └── helpers.py           # Shared utilities
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── model/
│   ├── phq9_pipeline.pkl
│   ├── shap_explainer.pkl
│   └── feature_names.json
├── data/
│   └── phq9.csv
├── notebooks/
│   └── train.py
├── tests/
│   ├── test_predictor.py
│   └── test_validators.py
├── config/
│   └── settings.py
├── wsgi.py
├── .env.example
├── requirements.txt
└── README.md
```

## Separation of Concerns

Separate logic into dedicated modules for:

- Route handling
- Model loading
- Prediction logic
- SHAP explanation generation
- Suggestion generation
- PDF report generation
- Utility helpers
- Configuration management

The system must avoid a monolithic architecture.

# Scalability and Performance Requirements

The application needs to:

- Support scalable deployment.
- Avoid irrelevant computation during inference.
- Optimize preprocessing pipelines for inference efficiency and consistency.
- Use reusable helper functions.
- Ensure predictions are generated quickly with minimal response delay.
- Support clean expansion of future features.

# Code Quality Requirements

The project needs to:

- Use clean and readable code.
- Follow modular design principles.
- Avoid repeated logic.
- Avoid hardcoded paths.
- Use reusable helper functions.
- Maintain clear naming conventions.
- Add docstrings where appropriate.
- Maintain a production-quality structure.

The codebase must not:

- Use fake placeholder logic.
- Invent nonexistent modules, APIs, datasets, or unsupported functionality.
- Include fabricated functionality.

# Error Handling Requirements

Handle gracefully:

- Invalid dataset schema
- Missing values
- Incorrect user inputs
- Improper predictions
- SHAP loading failure
- Failed PDF generation
- Unexpected backend processing failures

The system must:

- Return structured error responses.
- Log failures appropriately.
- Display user-friendly frontend errors accurately.

## Error Response Format

```json
{
  "error": true,
  "message": "User-safe description of the issue",
  "code": 400
}
```

# Technology Stack

## Machine Learning

Use:

- Python
- NumPy
- Pandas
- SHAP
- Scikit-learn
- XGBoost

## Backend

Use:

- Flask
- Gunicorn
- dotenv

## Frontend

Use:

- HTML
- CSS
- JavaScript

## Reporting

Use:

- ReportLab

## Optional Database Support

Optional database support:

- MongoDB
- PostgreSQL

# Output Requirements

Generate the project in the following order:

1. Directory structure
2. Source code for the training pipeline
3. Save/load logic
4. Flask backend implementation
5. HTML frontend
6. CSS styling
7. JavaScript frontend logic
8. SHAP explanation logic
9. PDF generation logic
10. `requirements.txt`
11. `README.md`
12. Installation instructions

If more than one file is generated:

- Send one file at a time.
- State filenames clearly.
- Make outputs modular and copyable.

# Documentation Requirements

Provide proper documentation for:

- Installation process
- Environment variables
- Workflow for model training
- How to run the Flask application
- Deployment steps
- Dependency installation

# Final Engineering Guidelines

- Maintain a professional, production-grade standard.
- Organize specifications into sections rather than paragraphs.
- Prioritize correctness, maintainability, and scalability.
- Ensure all elements follow the defined architecture.
- Build a realistic, production-like project.
- Maintain an ethical, calm, supportive, and emotionally safe tone throughout the system.
- Ensure the final implementation follows production-grade engineering standards with functional Explainable AI integration suitable for real-world deployment scenarios.