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
- Use the user-provided dataset at `data/phq9.csv` for all training and inference. Do not use synthetic data under any circumstances.

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

- Handle missing values appropriately. The imputation strategy used must be documented in code comments.
- Support categorical encoding (e.g., one-hot or ordinal as appropriate per column).
- Support numeric feature scaling if necessary.
- Prevent data leakage — all transformations must be fit only on training data, never on the full dataset.
- Maintain identical preprocessing during inference as during training.

## Validation Requirements

Include:

- Implement a proper train/test split strategy (e.g., 80/20).
- Model evaluation metrics: MAE, RMSE, and R² at minimum.
- Cross-validation if the dataset size warrants it.
- Proper schema validation checks before training and before inference.

The system must not:

- Create Fabricate dataset statistics.
- Invent evaluation metrics.
- Claim unsupported model performance.

# Machine Learning Requirements

## Model Objectives

Build a regression-based machine learning pipeline that:

- Predicts a continuous PHQ score.
- Uses Explainable AI techniques for interpretability.
- Supports reliable inference and scalable deployment.

## Severity Mapping

Map PHQ scores into:

- Minimal : 0-4
- Mild: 5-9
- Moderate: 10-14
- Moderately Severe:15-19
- Severe: 20-27

## Model Persistence

The system should save and cleanly load at startup:

- `model/phq9_pipeline.pkl` — trained preprocessing and model pipeline.
- `model/shap_explainer.pkl` — fitted SHAP explainer. Use `shap.TreeExplainer` for XGBoost. Fall back to `shap.KernelExplainer` only if necessary, with a documented reason.
- `model/feature_names.json` — ordered list of feature names used during training.

All artifacts must load at Flask startup without requiring retraining.

# Explainability Requirements

## SHAP Integration

Using SHAP to:

- Discover influential features per prediction.
- Rank influential features by SHAP contribution magnitude.
- Make prediction behavior understandable.

## Human-Readable Explanations

The explainability system must:

- Convert SHAP outputs into insights that are easy to understand.
- Use simple, emotionally safe language when explaining predictions to end users and avoid technical AI terminology.
- Generate explanations that are supportive and considerate of users' feelings.
- Be careful not to make things sound more certain than they really are.

## Example of required transformation

Wrong: "Feature 'sleep_quality' has a SHAP value of -1.43."  
Correct: "Sleep quality appeared to be a notable factor in your results. Difficulty sleeping can sometimes affect how we feel overall."

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

## Requirements for API

Implement backend routes for:

1. **Home Route**  
   Route: `/`  
   Method: `GET`  
   Purpose: Renders the home page of the application.

2. **Prediction Route**  
   Route: `/predict`  
   Method: `POST`  
   Purpose: Accepts user input payload and returns the prediction result in JSON format along with explanations.

3. **Report Generation Route**  
   Route: `/report`  
   Method: `POST`  
   Purpose: Accepts the prediction result and generates a downloadable PDF report.

4. **Health Check Route**  
   Route: `/health`  
   Method: `GET`  
   Purpose: Returns the system health status and confirms whether the ML model is loaded successfully.

## Functionality of Backend

The backend should do:

- Dynamically load trained models.
- Load SHAP explainers efficiently during runtime initialization.
- Incoming payloads should be validated.
- Predict PHQ scores.
- Generate severity levels.
- Produce proper explanations and suggestions.
- Structured JSON responses should be returned.

## Input Payload Schema

The `/predict` endpoint expects the following fields at minimum. Additional fields are inferred dynamically from the dataset schema:

```json
{
  "age": "integer, required, range 10–100",
  "gender": "string, required, one of [Male, Female, Other]",
  "sleep_quality": "integer, required, range 1–5",
  "study_pressure": "integer, required, range 1–5",
  "financial_pressure": "integer, required, range 1–5"
}

Security and Validations

It should implement:

Type and range validation on all inputs before inference.
Structured JSON error responses with appropriate HTTP status codes.
Safely parse and validate incoming requests
Use environment variables securely for configuration management.
Securely handle configuration
Frontend Requirements
Requirements for UI Design

Planning a clean responsive UI alongside healthcare design and the following features::

PHQ-9 questionnaire form
Registered age input
Gender input
Sleep quality input
Study pressure input
Financial pressure input
Result Display Requirements

Display:

Estimated PHQ Score
Severity level
Confidence level (clearly labeled as a calibrated estimate, not a certainty)
Severity category visualization
Confidence visualization bar
Explanation table (in plain, non-technical language)
Supportive recommendations
Medical disclaimer — always visible near results, not hidden
User Experience Requirements

The frontend should:

Be mobile-optimized.
Use accessible labels and fonts as well.
Allow the asynchronous submission of a form with fetch.
Display loading states gracefully.
Provide clear validation feedback for incomplete or invalid form inputs.
No page refreshes.
Present results in a calm and understandable way.
Animation and Interaction Requirements

Include:

Smooth transitions
User-friendly UI
Distraction-free animations
Performance-friendly rendering
Requirements for PDF Reporting

Generate downloadable PDF reports containing:

Date of assessment
PHQ score
Level of severity
Confidence prediction
Summary of risks
Key contributing factors affecting the prediction.
Support recommendations
Medical disclaimer
Requirements for PDF Design

Reports should be:

Printable
Structured
Professional
Easy to read

Use:

ReportLab
Architecture Requirements
Project Structure

Use a modular architecture like this:

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
Concerns for Separation

Separate logic into dedicated modules for:

Route handling
Model loading
Prediction logic
SHAP explanation generation
Suggestion generation
PDF report generation
Utility helpers
Configuration management

The system needs to avoid a monolithic architecture.

Requirements for Scalability and Performance

The application needs to:

Support a scalable deployment.
Avoid irrelevant computation during inference.
Optimize preprocessing pipelines for inference efficiency and consistency
It should use reusable helper functions.
It should ensure predictions are generated quickly with minimal response delay
Support the expansion of future features cleanly.
Requirements for Code Quality

The project needs to:

Use clean and readable code.
Follow the principle of modular design.
Try to avoid repeated logic.
Do not use hardcoded paths.
Use reusable helper functions.
Have clear naming conventions.
Add docstrings where appropriate.
Maintain production-quality structure.

The codebase must not:

Use fake placeholder logic.
Do not invent nonexistent modules, APIs, datasets, or unsupported functionality.
Include fabricated functionality.
Requirements for Error Handling

Handle elegantly:

The dataset schema is invalid
Values missing
False user inputs
Improper predictions
SHAP Loading Failure
Failed to generate PDF
Unexpected backend processing failures

The system must:

Return structured error responses.
Log failure as appropriate.
More accurate display of user-friendly frontend errors.

All error responses must follow this structure:

{
  "error": true,
  "message": "User-safe description of the issue",
  "code": 400
}
Technology Stack
For Machine Learning

Use:

Python
NumPy
Pandas
SHAP
Scikit-learn
XGBoost
For Backend

Use:

Flask
Gunicorn
dotenv
For Frontend

Use:

HTML
CSS
JavaScript
For Reporting

Use:

ReportLab
Optional Database Support

Optional database supports:

MongoDB
PostgreSQL
Requirements for Output

Generate the project in the following order:

The directory structure
The source code for the training pipeline
save/load logic
Flask backend implementation.
HTML front-end
Styling utilizing CSS
JavaScript frontend logic.
SHAP explanation logic
PDF generation logic
requirements.txt
README.md
Instructions for installation

If more than one file is generated:

Send that one file at a time.
State the filenames clearly.
Make outputs modular and copyable.
Requirements for Documentation

Provide proper documentation for:

Installation process
Environment variables
Workflow for model training
How to run the Flask application
Deployment steps
Install dependencies
Final Engineering Guidelines

Maintain a professional, production-grade standard.

Organize your specifications into sections rather than paragraphs.

Put correctness, maintainability, and scalability first.

Make sure that all elements follow the architecture you defined.

Realistic and production-like whole project.

Ensure the system maintains an ethical, calm, supportive, and emotionally safe tone.

The final implementation must follow production-grade engineering standards with functional Explainable AI integration suitable for real-world deployment scenarios