"""
Model loading utilities — loads and caches model artifacts on first access.
"""

import pickle
import threading
from typing import Any

from config.settings import MODEL_PATH, EXPLAINER_PATH, FEATURE_NAMES_PATH

_lock = threading.Lock()
_cache: dict[str, Any] = {}


def _load(path: str, key: str) -> Any:
    if key not in _cache:
        with _lock:
            if key not in _cache:
                with open(path, "rb") as f:
                    _cache[key] = pickle.load(f)
    return _cache[key]


def get_model():
    """Return the trained XGBoost regressor."""
    return _load(MODEL_PATH, "model")


def get_explainer():
    """Return the SHAP TreeExplainer."""
    return _load(EXPLAINER_PATH, "explainer")


def get_feature_names() -> list[str]:
    """Return the ordered list of feature names used during training."""
    return _load(FEATURE_NAMES_PATH, "feature_names")
