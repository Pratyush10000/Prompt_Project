"""
Training pipeline for PHQ-9 regression model.

Run:  python train.py
Output: model/xgb_model.pkl, model/shap_explainer.pkl, model/feature_names.pkl
"""

import os
import sys
import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.preprocessing import OrdinalEncoder
import xgboost as xgb
import shap

warnings.filterwarnings("ignore")

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.settings import (
    DATA_PATH, MODEL_PATH, EXPLAINER_PATH, FEATURE_NAMES_PATH,
    PHQ_ANSWER_MAP, QUALITY_MAP, GENDER_MAP,
)


# ─────────────────────────────────────────────
# 1. LOAD & VALIDATE
# ─────────────────────────────────────────────

def load_and_validate(path: str) -> pd.DataFrame:
    """Load CSV and assert expected columns exist."""
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]  # strip surrounding whitespace

    required = {"Age", "Gender", "PHQ_Total", "Sleep Quality", "Study Pressure", "Financial Pressure"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")

    print(f"[train] Loaded {len(df)} rows, {len(df.columns)} columns.")
    return df


# ─────────────────────────────────────────────
# 2. IDENTIFY PHQ QUESTION COLUMNS
# ─────────────────────────────────────────────

KNOWN_NON_PHQ = {
    "Age", "Gender", "PHQ_Total", "PHQ_Severity",
    "Sleep Quality", "Study Pressure", "Financial Pressure",
}

def get_phq_columns(df: pd.DataFrame) -> list[str]:
    """Return the 9 PHQ item columns in original order."""
    phq_cols = [c for c in df.columns if c not in KNOWN_NON_PHQ]
    assert len(phq_cols) == 9, f"Expected 9 PHQ item columns, found {len(phq_cols)}: {phq_cols}"
    return phq_cols


# ─────────────────────────────────────────────
# 3. PREPROCESSING
# ─────────────────────────────────────────────

def preprocess(df: pd.DataFrame, phq_cols: list[str]) -> tuple[pd.DataFrame, pd.Series]:
    """Encode all features and return (X, y)."""
    df = df.copy()

    # Encode PHQ item answers
    for col in phq_cols:
        df[col] = df[col].str.strip().map(PHQ_ANSWER_MAP)
        if df[col].isna().any():
            raise ValueError(f"Unexpected PHQ answer values in column '{col}'")

    # Encode contextual features
    df["Gender"] = df["Gender"].str.strip().map(GENDER_MAP)
    df["Sleep Quality"] = df["Sleep Quality"].str.strip().map(QUALITY_MAP)
    df["Study Pressure"] = df["Study Pressure"].str.strip().map(QUALITY_MAP)
    df["Financial Pressure"] = df["Financial Pressure"].str.strip().map(QUALITY_MAP)

    # Short feature names for interpretability
    rename = {col: f"phq{i+1}" for i, col in enumerate(phq_cols)}
    rename.update({
        "Sleep Quality": "sleep_quality",
        "Study Pressure": "study_pressure",
        "Financial Pressure": "financial_pressure",
        "Gender": "gender",
        "Age": "age",
    })
    df = df.rename(columns=rename)

    feature_cols = [f"phq{i}" for i in range(1, 10)] + [
        "sleep_quality", "study_pressure", "financial_pressure", "gender", "age"
    ]

    X = df[feature_cols]
    y = df["PHQ_Total"]

    print(f"[train] Features: {feature_cols}")
    print(f"[train] Target range: {y.min()}–{y.max()}, mean={y.mean():.2f}")
    return X, y, feature_cols


# ─────────────────────────────────────────────
# 4. TRAIN & EVALUATE
# ─────────────────────────────────────────────

def train_model(X: pd.DataFrame, y: pd.Series) -> tuple[xgb.XGBRegressor, dict]:
    """Train XGBoost regressor with cross-validation, return model and metrics."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = xgb.XGBRegressor(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        verbosity=0,
    )
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    y_pred = model.predict(X_test)

    # Cross-validation MAE
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")
    cv_mae = -cv_scores.mean()

    metrics = {
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "r2": float(r2_score(y_test, y_pred)),
        "cv_mae_5fold": float(cv_mae),
    }
    print(f"[train] Metrics: {metrics}")
    return model, metrics


# ─────────────────────────────────────────────
# 5. SHAP EXPLAINER
# ─────────────────────────────────────────────

def build_explainer(model: xgb.XGBRegressor, X: pd.DataFrame) -> shap.TreeExplainer:
    """Build and return a SHAP TreeExplainer."""
    explainer = shap.TreeExplainer(model, feature_perturbation="interventional", data=X)
    print("[train] SHAP TreeExplainer built.")
    return explainer


# ─────────────────────────────────────────────
# 6. SAVE ARTIFACTS
# ─────────────────────────────────────────────

def save_artifacts(model, explainer, feature_names: list[str]) -> None:
    """Persist model, explainer, and feature names."""
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(EXPLAINER_PATH, "wb") as f:
        pickle.dump(explainer, f)
    with open(FEATURE_NAMES_PATH, "wb") as f:
        pickle.dump(feature_names, f)
    print(f"[train] Saved model → {MODEL_PATH}")
    print(f"[train] Saved explainer → {EXPLAINER_PATH}")
    print(f"[train] Saved feature names → {FEATURE_NAMES_PATH}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    df = load_and_validate(DATA_PATH)
    phq_cols = get_phq_columns(df)
    X, y, feature_names = preprocess(df, phq_cols)
    model, metrics = train_model(X, y)
    explainer = build_explainer(model, X)
    save_artifacts(model, explainer, feature_names)
    print("[train] Training pipeline complete.")
    print(f"[train] Final metrics: {metrics}")
