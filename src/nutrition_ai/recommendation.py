from __future__ import annotations

from .schemas import UserProfile


def recommendation_notes(profile: UserProfile, prediction: dict[str, float]) -> list[str]:
    notes: list[str] = []

    if profile.sleep_hours < 6.5:
        notes.append("Duermes poco: intenta subir a 7-9h para mejorar recuperación y adherencia.")

    if profile.stress_level >= 4:
        notes.append(
            "Estrés alto detectado: considera empezar con mantenimiento antes de déficit agresivo."
        )

    if profile.goal == "definicion" and prediction["calories"] < 1400:
        notes.append("Tu caloría recomendada es baja. Revisa con un profesional para evitar déficit excesivo.")

    if profile.sports_experience_years < 1:
        notes.append(
            "Como principiante, prioriza constancia y técnica. Ajusta calorías cada 2-3 semanas."
        )

    if not notes:
        notes.append("Plan equilibrado: monitoriza peso/medidas y ajusta ±150 kcal según evolución.")

    return notes
