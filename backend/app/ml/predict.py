from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np

from app.core.config import settings


_MODEL = None


def _load_model():
    global _MODEL
    if _MODEL is None:
        model_path = Path(settings.MODEL_PATH)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {model_path}. Train it with: python backend/scripts/train_model.py"
            )
        _MODEL = joblib.load(model_path)
    return _MODEL


def predict_risk_percent(
    rainfall_mm: float, humidity: float, river_level_m: float, drainage_capacity: float
) -> float:
    """
    Uses the trained scikit-learn model if present.
    If model isn't available (or sklearn/scipy is problematic on a machine),
    we fall back to a deterministic heuristic so the app still works.
    """
    try:
        model = _load_model()
        x = np.array([[rainfall_mm, humidity, river_level_m, drainage_capacity]], dtype=float)
        proba = model.predict_proba(x)[0, 1]
        return float(np.clip(proba * 100.0, 0.0, 100.0))
    except Exception:
        # Heuristic fallback: scaled sigmoid of a latent score.
        latent = (
            0.012 * float(rainfall_mm)
            + 0.020 * float(humidity)
            + 0.35 * float(river_level_m)
            - 0.018 * float(drainage_capacity)
            + 0.00008 * (float(rainfall_mm) * float(humidity))
        )
        prob = 1.0 / (1.0 + np.exp(-(latent - 2.5)))
        return float(np.clip(prob * 100.0, 0.0, 100.0))


def risk_level_from_percent(risk_percent: float) -> str:
    if risk_percent >= 80:
        return "High"
    if risk_percent >= 50:
        return "Medium"
    return "Low"

