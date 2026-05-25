"""
Application configuration: constants, mappings, and feature definitions.
"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "phq9.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "xgb_model.pkl")
EXPLAINER_PATH = os.path.join(BASE_DIR, "model", "shap_explainer.pkl")
FEATURE_NAMES_PATH = os.path.join(BASE_DIR, "model", "feature_names.pkl")

# PHQ-9 question ordinal mapping (0–3 scale)
PHQ_ANSWER_MAP = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3,
}

# Ordinal pressure/quality scales
QUALITY_MAP = {
    "Good": 0,
    "Average": 1,
    "Bad": 2,
    "Worst": 3,
}

GENDER_MAP = {
    "Male": 0,
    "Female": 1,
}

# PHQ score → severity label
SEVERITY_BANDS = [
    (0, 4, "Minimal"),
    (5, 9, "Mild"),
    (10, 14, "Moderate"),
    (15, 19, "Moderately Severe"),
    (20, 27, "Severe"),
]

# Friendly short names for PHQ-9 items (used in explanations)
PHQ_ITEM_LABELS = {
    "phq1": "Low interest or pleasure",
    "phq2": "Feeling down or hopeless",
    "phq3": "Sleep difficulties",
    "phq4": "Low energy or fatigue",
    "phq5": "Appetite changes",
    "phq6": "Feelings of failure or guilt",
    "phq7": "Concentration difficulties",
    "phq8": "Psychomotor changes",
    "phq9": "Thoughts of self-harm",
    "sleep_quality": "Sleep quality",
    "study_pressure": "Study pressure",
    "financial_pressure": "Financial pressure",
    "age": "Age",
    "gender": "Gender",
}

# Supportive suggestions keyed by feature name
SUGGESTIONS = {
    "phq1": "Try small, enjoyable activities — even a short walk or a favourite song can help reconnect with pleasure.",
    "phq2": "Speaking with someone you trust about how you are feeling can ease emotional heaviness.",
    "phq3": "A consistent sleep schedule and reducing screen time before bed often improve rest quality.",
    "phq4": "Gentle movement, hydration, and brief outdoor exposure can support energy levels.",
    "phq5": "Eating at regular times — even small, nourishing meals — helps maintain mood stability.",
    "phq6": "Self-compassion exercises and reframing self-talk can soften harsh inner criticism.",
    "phq7": "Short, focused work intervals (e.g., 25-minute Pomodoro sessions) can support concentration.",
    "phq8": "Mindfulness or light stretching can help when restlessness or slowness is noticeable.",
    "phq9": "If difficult thoughts arise, please reach out to a trusted person or a support helpline.",
    "sleep_quality": "Improving sleep hygiene — regular hours, a dark room, and winding-down routines — can have a broad positive effect.",
    "study_pressure": "Breaking tasks into smaller steps and scheduling planned breaks can reduce academic pressure.",
    "financial_pressure": "Talking to a student counsellor or financial advisor can open up options you may not be aware of.",
    "age": "Remember that many people your age navigate similar challenges — you are not alone.",
    "gender": "Support networks tailored to your community and identity can be especially helpful.",
}

# General fallback suggestion
GENERAL_SUGGESTION = (
    "Consider speaking with a counsellor or mental health professional for personalised guidance. "
    "This assessment is an awareness tool, not a diagnosis."
)
