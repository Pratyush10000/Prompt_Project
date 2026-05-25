"""
Prediction service: wraps model inference, SHAP explanation, severity mapping,
confidence estimation, and suggestion generation.
"""

import numpy as np
import pandas as pd
import shap

from config.settings import SEVERITY_BANDS, PHQ_ITEM_LABELS, SUGGESTIONS, GENERAL_SUGGESTION
from utils.model_loader import get_model, get_explainer, get_feature_names
from utils.preprocessing import encode_input


# ─────────────────────────────────────────────
# SEVERITY
# ─────────────────────────────────────────────

def map_severity(score: float) -> str:
    """Map a continuous PHQ score to a severity label."""
    clamped = max(0.0, min(27.0, score))
    for lo, hi, label in SEVERITY_BANDS:
        if lo <= clamped <= hi:
            return label
    return "Severe"


# ─────────────────────────────────────────────
# CONFIDENCE
# ─────────────────────────────────────────────

def estimate_confidence(score: float, shap_values: np.ndarray) -> float:
    """
    Estimate a calibrated confidence score (0–1) using prediction stability.

    Confidence is derived from the ratio of the top explanatory signal
    to total SHAP magnitude — higher agreement between features → higher confidence.
    This is a heuristic measure of internal consistency, not a probabilistic guarantee.
    """
    abs_shap = np.abs(shap_values)
    total = abs_shap.sum()
    if total < 1e-6:
        return 0.75  # Default when all SHAP values are near zero
    top_k = np.sort(abs_shap)[::-1][:5].sum()
    raw = float(top_k / total)
    # Rescale to [0.60, 0.95] — avoids overconfidence
    confidence = 0.60 + raw * 0.35
    return round(min(0.95, max(0.60, confidence)), 3)


# ─────────────────────────────────────────────
# EXPLANATION TEXT
# ─────────────────────────────────────────────

def generate_explanation(feature_names: list[str], shap_values: np.ndarray, top_k: int = 5) -> list[dict]:
    """
    Return top-k features ranked by SHAP magnitude with human-readable descriptions.

    Each item: { feature, label, direction, shap_value, explanation }
    """
    abs_vals = np.abs(shap_values)
    ranked_idx = np.argsort(abs_vals)[::-1][:top_k]

    results = []
    for idx in ranked_idx:
        feat = feature_names[idx]
        sv = float(shap_values[idx])
        label = PHQ_ITEM_LABELS.get(feat, feat)
        direction = "increased" if sv > 0 else "decreased"
        magnitude = abs(sv)

        if magnitude < 0.05:
            continue  # Skip negligible contributors

        if sv > 0:
            phrase = f"Your responses around '{label}' appear to be contributing to a higher distress estimate."
        else:
            phrase = f"Your responses around '{label}' appear to be a supportive factor in your current wellbeing."

        results.append({
            "feature": feat,
            "label": label,
            "direction": direction,
            "shap_value": round(sv, 3),
            "explanation": phrase,
        })

    return results


# ─────────────────────────────────────────────
# SUGGESTIONS
# ─────────────────────────────────────────────

def generate_suggestions(explanation_items: list[dict]) -> list[str]:
    """Return personalised suggestions based on the top SHAP features."""
    seen = set()
    suggestions = []
    for item in explanation_items:
        if item["direction"] == "increased":
            feat = item["feature"]
            if feat not in seen and feat in SUGGESTIONS:
                suggestions.append(SUGGESTIONS[feat])
                seen.add(feat)
    if not suggestions:
        suggestions.append(GENERAL_SUGGESTION)
    suggestions.append(GENERAL_SUGGESTION)
    return suggestions


# ─────────────────────────────────────────────
# MAIN PREDICTION ENTRY POINT
# ─────────────────────────────────────────────

def predict(raw_input: dict) -> dict:
    """
    Run full inference pipeline and return a structured result dict.

    Parameters
    ----------
    raw_input : dict
        Raw form data from the frontend.

    Returns
    -------
    dict with keys: phq_score, severity, confidence, explanation, suggestions
    """
    model = get_model()
    explainer = get_explainer()
    feature_names = get_feature_names()

    X = encode_input(raw_input, feature_names)

    # Predict
    raw_score = float(model.predict(X)[0])
    phq_score = round(max(0.0, min(27.0, raw_score)), 1)
    severity = map_severity(phq_score)

    # SHAP
    shap_values = explainer(X).values[0]  # shape: (n_features,)

    confidence = estimate_confidence(phq_score, shap_values)
    explanation = generate_explanation(feature_names, shap_values)
    suggestions = generate_suggestions(explanation)

    return {
        "phq_score": phq_score,
        "severity": severity,
        "confidence": confidence,
        "explanation": explanation,
        "suggestions": suggestions,
    }
