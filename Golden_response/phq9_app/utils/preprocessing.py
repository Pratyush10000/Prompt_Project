"""
Preprocessing helpers for converting raw form input into model-ready features.
"""

import pandas as pd
from config.settings import PHQ_ANSWER_MAP, QUALITY_MAP, GENDER_MAP


def encode_input(raw: dict, feature_names: list[str]) -> pd.DataFrame:
    """
    Encode raw user input into a DataFrame aligned with training feature order.

    Parameters
    ----------
    raw : dict
        Keys: phq1–phq9 (str answers), age (int), gender (str),
              sleep_quality (str), study_pressure (str), financial_pressure (str)
    feature_names : list[str]
        Ordered feature names from training.

    Returns
    -------
    pd.DataFrame  (1 row, columns = feature_names)
    """
    encoded = {}

    for i in range(1, 10):
        key = f"phq{i}"
        val = str(raw.get(key, "Not at all")).strip()
        if val not in PHQ_ANSWER_MAP:
            raise ValueError(f"Invalid answer for {key}: '{val}'")
        encoded[key] = PHQ_ANSWER_MAP[val]

    for feat, mapping in [
        ("sleep_quality", QUALITY_MAP),
        ("study_pressure", QUALITY_MAP),
        ("financial_pressure", QUALITY_MAP),
    ]:
        val = str(raw.get(feat, "Average")).strip()
        if val not in mapping:
            raise ValueError(f"Invalid value for {feat}: '{val}'")
        encoded[feat] = mapping[val]

    gender_val = str(raw.get("gender", "Male")).strip()
    if gender_val not in GENDER_MAP:
        raise ValueError(f"Invalid gender value: '{gender_val}'")
    encoded["gender"] = GENDER_MAP[gender_val]

    try:
        encoded["age"] = int(raw.get("age", 20))
    except (TypeError, ValueError):
        raise ValueError("Age must be an integer.")

    df = pd.DataFrame([encoded])[feature_names]
    return df


def validate_payload(data: dict) -> list[str]:
    """
    Return a list of validation error messages for a raw input dict.
    Returns an empty list if the payload is valid.
    """
    errors = []
    for i in range(1, 10):
        key = f"phq{i}"
        if key not in data:
            errors.append(f"Missing field: {key}")
        elif data[key] not in PHQ_ANSWER_MAP:
            errors.append(f"Invalid answer for {key}: '{data[key]}'")

    for feat in ("sleep_quality", "study_pressure", "financial_pressure"):
        if feat not in data:
            errors.append(f"Missing field: {feat}")
        elif data[feat] not in QUALITY_MAP:
            errors.append(f"Invalid value for {feat}: '{data[feat]}'")

    if "gender" not in data:
        errors.append("Missing field: gender")
    elif data["gender"] not in GENDER_MAP:
        errors.append(f"Invalid gender value: '{data['gender']}'")

    if "age" not in data:
        errors.append("Missing field: age")
    else:
        try:
            age = int(data["age"])
            if not (10 <= age <= 100):
                errors.append("Age must be between 10 and 100.")
        except (TypeError, ValueError):
            errors.append("Age must be an integer.")

    return errors
