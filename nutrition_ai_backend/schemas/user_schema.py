from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class UserInput(BaseModel):
    age: int = Field(ge=14, le=90)
    weight: float = Field(ge=35, le=300, description="Peso en kg")
    height: float = Field(ge=130, le=230, description="Estatura en cm")
    gender: Literal["male", "female"]

    body_fat: float | None = Field(default=None, ge=3, le=60)
    activity_level: Literal["sedentary", "light", "moderate", "high", "very_high"]
    training_days: int = Field(ge=0, le=14)
    training_type: Literal[
        "none", "strength", "hypertrophy", "crossfit", "endurance", "mixed"
    ] = "mixed"
    training_experience_years: float = Field(default=0, ge=0, le=50)
    sports_history: bool = Field(
        default=False, description="Historial deportivo previo importante"
    )

    goal: Literal["bulk", "maintenance", "cut"]
    sleep_hours: float = Field(ge=3, le=12)
    stress_level: int = Field(ge=1, le=5)

    body_type: Literal["ectomorph", "mesomorph", "endomorph", "unknown"] = "unknown"
    avg_daily_steps: int = Field(default=7000, ge=0, le=50000)
    work_type: Literal["sedentary", "active", "physical"] = "sedentary"
    metabolic_rate_factor: float = Field(
        default=1.0,
        ge=0.85,
        le=1.15,
        description="Ajuste metabólico estimado (1.0=normal)",
    )
