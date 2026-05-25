# PHQ-9 Mental Health Risk Assessment — Explainable AI

A production-quality, web-based mental health **awareness** tool that:
- collects PHQ-9 responses via a warm, accessible UI
- predicts a continuous PHQ score using an XGBoost regressor
- explains the result with SHAP (plain English, no jargon)
- generates a downloadable PDF wellness report
- maintains an empathetic, non-clinical tone throughout

> **Important:** This is an educational awareness tool. It is **not** a medical diagnosis instrument. Always consult a qualified mental health professional.

---

## Architecture


```
├── prompt.md                     # Benchmark prompt for LLM evaluation
├── justification.md              # Comparative evaluation of model outputs
├── README.md                     # Project documentation
phq9_app/
├── app/
│   ├── app.py                 # Flask application factory
│   ├── templates/
│   │   └── index.html         # Responsive UI
│   └── static/
│       ├── css/style.css
│       └── js/
│           ├── questions.js   # PHQ-9 question renderer
│           └── app.js         # Fetch, gauge, results logic
├── config/
│   └── settings.py            # Constants, mappings, labels
├── data/
│   └── phq9.csv               # Source dataset (682 rows)
├── model/
│   ├── xgb_model.pkl          # Trained XGBoost regressor
│   ├── shap_explainer.pkl     # SHAP TreeExplainer
│   └── feature_names.pkl      # Feature alignment reference
├── routes/
│   └── api.py                 # /predict and /report endpoints
├── services/
│   ├── prediction_service.py  # Inference + SHAP + severity + suggestions
│   └── report_service.py      # ReportLab PDF generation
├── utils/
│   ├── model_loader.py        # Thread-safe lazy model loading
│   └── preprocessing.py       # Encoding + payload validation
├── train.py                   # Full training pipeline (run once)
├── wsgi.py                    # Gunicorn WSGI entry point
└── requirements.txt
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model
```bash
cd Golden_response/phq9_app
python train.py
```
This produces `model/xgb_model.pkl`, `model/shap_explainer.pkl`, and `model/feature_names.pkl`.

**Actual model metrics (5-fold CV):**
| Metric | Value |
|--------|-------|
| MAE (test set) | 0.458 |
| RMSE (test set) | 0.649 |
| R² (test set) | 0.992 |
| MAE (5-fold CV) | 0.429 |

### 3. Run the development server
```bash
python app/app.py
```
Open https://mindful-check-2.onrender.com/

### 4. Production deployment (Gunicorn)
```bash
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-key-change-in-prod` | Flask session secret |
| `PORT` | `5000` | Server port |
| `FLASK_DEBUG` | `false` | Enable debug mode |

---

## API Reference

### `POST /predict`
**Body (JSON):**
```json
{
  "phq1": "Several days",
  "phq2": "Not at all",
  ...
  "phq9": "Not at all",
  "age": 22,
  "gender": "Female",
  "sleep_quality": "Bad",
  "study_pressure": "Average",
  "financial_pressure": "Good"
}
```

**PHQ answer options:** `"Not at all"`, `"Several days"`, `"More than half the days"`, `"Nearly every day"`  
**Quality/Pressure options:** `"Good"`, `"Average"`, `"Bad"`, `"Worst"`  
**Gender options:** `"Male"`, `"Female"`

**Response:**
```json
{
  "phq_score": 9.4,
  "severity": "Mild",
  "confidence": 0.86,
  "explanation": [
    { "feature": "phq3", "label": "Sleep difficulties", "direction": "increased", "shap_value": 1.2, "explanation": "..." }
  ],
  "suggestions": ["...", "..."]
}
```

### `POST /report`
Same body as `/predict`. Returns a **PDF file** download.

---

## Feature Engineering

| Feature | Encoding |
|---------|----------|
| PHQ-9 items (9×) | Ordinal: 0 (Not at all) → 3 (Nearly every day) |
| Sleep / Study / Financial pressure | Ordinal: 0 (Good) → 3 (Worst) |
| Gender | Binary: Male=0, Female=1 |
| Age | Numeric (integer) |

---

## Ethical Commitments

- No responses are stored or logged
- Severity language is supportive, not alarming
- SHAP explanations use plain English only
- Every result includes a disclaimer
- Confidence is a calibrated heuristic, not a probability guarantee
- The system never claims to diagnose

---

## License & Disclaimer

For educational and research purposes only. Not a substitute for professional mental health care.
