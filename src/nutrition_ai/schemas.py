from dataclasses import dataclass


@dataclass
class UserProfile:
    age: int
    weight_kg: float
    height_cm: float
    gender: str
    goal: str
    activity_level: str
    sleep_hours: float
    sports_experience_years: float
    body_fat_pct: float
    stress_level: int
