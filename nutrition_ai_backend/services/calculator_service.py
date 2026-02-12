from __future__ import annotations

from nutrition_ai_backend.models.nutrition_engine import adjust_for_goal, calculate_tdee
from nutrition_ai_backend.schemas.user_schema import UserInput


def _protein_per_kg(user: UserInput) -> float:
    if user.goal == "cut":
        return 2.0 if user.training_type in {"none", "endurance"} else 2.2
    if user.goal == "bulk":
        return 1.8 if user.training_type in {"strength", "hypertrophy"} else 1.7
    return 1.8


def _fat_per_kg(user: UserInput) -> float:
    if user.goal == "cut":
        return 0.8
    if user.goal == "bulk":
        return 0.9
    return 0.85


def calculate_macros(user: UserInput, target_calories: float) -> dict[str, float]:
    protein = user.weight * _protein_per_kg(user)
    fats = user.weight * _fat_per_kg(user)

    protein_cal = protein * 4
    fat_cal = fats * 9

    carbs = max((target_calories - (protein_cal + fat_cal)) / 4, user.weight * 1.0)

    return {
        "calories": round(target_calories),
        "protein_g": round(protein),
        "fats_g": round(fats),
        "carbs_g": round(carbs),
    }


def _coach_notes(user: UserInput) -> list[str]:
    notes: list[str] = []

    if user.sleep_hours < 6.5:
        notes.append("Sube el sueño a 7-9h: mejor recuperación y mejor partición de nutrientes.")
    if user.stress_level >= 4:
        notes.append("Estrés alto: usa progresión conservadora y revisa adherencia semanal.")
    if user.avg_daily_steps < 5000:
        notes.append("Pasos bajos: subir actividad NEAT mejorará mantenimiento de grasa.")
    if user.goal == "cut" and user.training_days < 3:
        notes.append("En definición conviene entrenar fuerza al menos 3 días/semana.")

    if not notes:
        notes.append("Buena base. Ajusta +/-150 kcal cada 2 semanas según progreso real.")

    return notes


def calculate_nutrition(user: UserInput) -> dict[str, float | dict[str, float] | list[str]]:
    tdee = calculate_tdee(user)
    target_calories, goal_factor = adjust_for_goal(tdee, user.goal, user.body_fat)
    macros = calculate_macros(user, target_calories)

    return {
        "inputs": user.model_dump(),
        "tdee": round(tdee),
        "goal_factor": round(goal_factor, 3),
        "targets": macros,
        "notes": _coach_notes(user),
        "engine": "deterministic_v1_ready_for_future_ml",
    }
