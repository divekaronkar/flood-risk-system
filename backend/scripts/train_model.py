import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# Allow running as: `python backend/scripts/train_model.py`
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def synthesize_dataset(n: int = 6000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    rainfall = rng.gamma(shape=2.0, scale=25.0, size=n).clip(0, 250)  # mm
    humidity = rng.normal(loc=70, scale=15, size=n).clip(0, 100)  # %
    river_level = rng.normal(loc=3.0, scale=1.3, size=n).clip(0, 10)  # meters
    drainage = rng.normal(loc=55, scale=18, size=n).clip(0, 100)  # capacity score

    # A simple "physics-inspired" latent risk score for labeling.
    # Higher rainfall/humidity/river level increases risk; higher drainage reduces risk.
    latent = (
        0.012 * rainfall
        + 0.020 * humidity
        + 0.35 * river_level
        - 0.018 * drainage
        + 0.00008 * (rainfall * humidity)
    )
    prob = 1.0 / (1.0 + np.exp(-(latent - 2.5)))
    y = rng.binomial(1, prob)

    return pd.DataFrame(
        {
            "rainfall_mm": rainfall,
            "humidity": humidity,
            "river_level_m": river_level,
            "drainage_capacity": drainage,
            "flood": y,
        }
    )


def main() -> None:
    df = synthesize_dataset()
    x = df[["rainfall_mm", "humidity", "river_level_m", "drainage_capacity"]].values
    y = df["flood"].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

    base = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        random_state=42,
        class_weight="balanced",
    )
    # Calibrate so that predicted "% risk" behaves more like a probability.
    model = CalibratedClassifierCV(base, method="isotonic", cv=3)
    model.fit(x_train, y_train)

    auc = roc_auc_score(y_test, model.predict_proba(x_test)[:, 1])
    print(f"ROC-AUC: {auc:.3f}")

    out_path = Path(__file__).resolve().parents[1] / "app" / "ml" / "model.joblib"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_path)
    print(f"Saved model to: {out_path}")


if __name__ == "__main__":
    main()

