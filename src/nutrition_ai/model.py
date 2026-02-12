from __future__ import annotations

from dataclasses import asdict

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .schemas import UserProfile


ACTIVITY_FACTORS = {
    "sedentario": 1.2,
    "ligero": 1.375,
    "moderado": 1.55,
    "alto": 1.725,
    "atleta": 1.9,
}

GOAL_ADJUSTMENTS = {
    "definicion": -0.20,
    "mantenimiento": 0.0,
    "volumen": 0.15,
}


def _build_features(rng: np.random.Generator, rows: int) -> pd.DataFrame:
    data = pd.DataFrame(
        {
            "age": rng.integers(18, 66, size=rows),
            "weight_kg": rng.uniform(45, 130, size=rows),
            "height_cm": rng.uniform(150, 205, size=rows),
            "gender": rng.choice(["hombre", "mujer"], size=rows, p=[0.55, 0.45]),
            "goal": rng.choice(["definicion", "mantenimiento", "volumen"], size=rows),
            "activity_level": rng.choice(list(ACTIVITY_FACTORS.keys()), size=rows),
            "sleep_hours": rng.uniform(4.0, 9.5, size=rows),
            "sports_experience_years": rng.uniform(0, 25, size=rows),
            "body_fat_pct": rng.uniform(7, 40, size=rows),
            "stress_level": rng.integers(1, 6, size=rows),
        }
    )
    return data


def _formula_targets(data: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    male_const = np.where(data["gender"] == "hombre", 5, -161)
    bmr = 10 * data["weight_kg"] + 6.25 * data["height_cm"] - 5 * data["age"] + male_const

    activity = data["activity_level"].map(ACTIVITY_FACTORS)
    goal = data["goal"].map(GOAL_ADJUSTMENTS)

    sleep_effect = np.clip((data["sleep_hours"] - 7) * 0.015, -0.05, 0.03)
    experience_effect = np.clip(data["sports_experience_years"] * 0.002, 0, 0.04)
    stress_effect = np.clip((3 - data["stress_level"]) * 0.01, -0.03, 0.02)

    calories = bmr * activity * (1 + goal + sleep_effect + experience_effect + stress_effect)

    lean_factor = np.clip((100 - data["body_fat_pct"]) / 100, 0.55, 0.95)
    protein_g = (1.6 + np.where(data["goal"] == "volumen", 0.4, 0.2)) * data["weight_kg"] * lean_factor
    fat_g = np.where(data["goal"] == "definicion", 0.8, 0.95) * data["weight_kg"]
    carbs_g = np.maximum((calories - protein_g * 4 - fat_g * 9) / 4, data["weight_kg"] * 1.5)

    noise = rng.normal(0, [90, 8, 6, 18], size=(len(data), 4))
    targets = pd.DataFrame(
        {
            "calories": calories + noise[:, 0],
            "protein_g": protein_g + noise[:, 1],
            "fat_g": fat_g + noise[:, 2],
            "carbs_g": carbs_g + noise[:, 3],
        }
    )
    return targets.clip(lower=0)


class NutritionRegressor:
    """Pequeña red neuronal para aproximar objetivos nutricionales personalizados."""

    def __init__(self) -> None:
        self.pipeline = self._build_pipeline()

    @staticmethod
    def _build_pipeline() -> Pipeline:
        numeric = [
            "age",
            "weight_kg",
            "height_cm",
            "sleep_hours",
            "sports_experience_years",
            "body_fat_pct",
            "stress_level",
        ]
        categorical = ["gender", "goal", "activity_level"]

        preprocessor = ColumnTransformer(
            [
                ("num", StandardScaler(), numeric),
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ]
        )

        model = MultiOutputRegressor(
            MLPRegressor(
                hidden_layer_sizes=(64, 32),
                activation="relu",
                max_iter=900,
                random_state=42,
            )
        )

        return Pipeline([("prep", preprocessor), ("model", model)])

    def fit(self, rows: int = 6000, random_seed: int = 42) -> None:
        rng = np.random.default_rng(random_seed)
        features = _build_features(rng, rows)
        targets = _formula_targets(features, rng)
        self.pipeline.fit(features, targets)

    def predict(self, profile: UserProfile) -> dict[str, float]:
        features = pd.DataFrame([asdict(profile)])
        raw = self.pipeline.predict(features)[0]

        result = {
            "calories": float(raw[0]),
            "protein_g": float(raw[1]),
            "fat_g": float(raw[2]),
            "carbs_g": float(raw[3]),
        }
        return {k: round(max(v, 0.0), 1) for k, v in result.items()}
