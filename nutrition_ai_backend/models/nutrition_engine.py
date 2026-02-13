from __future__ import annotations

from nutrition_ai_backend.schemas.user_schema import UserInput


ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "high": 1.725,
    "very_high": 1.9,
}

GOAL_RANGES = {
    "bulk": (1.10, 1.20),
    "maintenance": (1.0, 1.0),
    "cut": (0.75, 0.85),
}


def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """Mifflin-St Jeor."""
    if gender == "male":
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    return (10 * weight) + (6.25 * height) - (5 * age) - 161


def _neat_adjustment(user: UserInput) -> float:
    steps_delta = (user.avg_daily_steps - 7000) / 10000 * 0.06
    work_bonus = {"sedentary": 0.0, "active": 0.04, "physical": 0.08}[user.work_type]
    return max(-0.08, min(0.15, steps_delta + work_bonus))


def _recovery_adjustment(user: UserInput) -> float:
    sleep_effect = max(-0.06, min(0.03, (user.sleep_hours - 7.0) * 0.015))
    stress_effect = max(-0.04, min(0.03, (3 - user.stress_level) * 0.015))
    exp_effect = max(0.0, min(0.04, user.training_experience_years * 0.004))
    sports_history_effect = 0.02 if user.sports_history else 0.0
    return sleep_effect + stress_effect + exp_effect + sports_history_effect


def _training_adjustment(user: UserInput) -> float:
    day_effect = max(0.0, min(0.08, user.training_days * 0.012))
    type_effect = {
        "none": -0.03,
        "strength": 0.03,
        "hypertrophy": 0.04,
        "crossfit": 0.05,
        "endurance": 0.03,
        "mixed": 0.04,
    }[user.training_type]
    return day_effect + type_effect


def calculate_tdee(user: UserInput) -> float:
    bmr = calculate_bmr(user.weight, user.height, user.age, user.gender)
    base = bmr * ACTIVITY_MULTIPLIERS[user.activity_level]

    adjustment = _neat_adjustment(user) + _recovery_adjustment(user) + _training_adjustment(user)
    adjusted = base * (1 + adjustment) * user.metabolic_rate_factor
    return max(adjusted, bmr * 1.1)


def adjust_for_goal(tdee: float, goal: str, body_fat: float | None = None) -> tuple[float, float]:
    low, high = GOAL_RANGES[goal]

    if goal == "cut" and body_fat is not None:
        # Más grasa -> déficit algo mayor dentro del rango seguro.
        normalized = max(0.0, min(1.0, (body_fat - 10) / 25))
        factor = high - (high - low) * normalized
    elif goal == "bulk" and body_fat is not None:
        # Más grasa -> superávit más conservador.
        normalized = max(0.0, min(1.0, (body_fat - 10) / 20))
        factor = high - (high - low) * normalized
    else:
        factor = (low + high) / 2

    calories = tdee * factor
    return calories, factor
