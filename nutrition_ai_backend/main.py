from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from nutrition_ai_backend.schemas.user_schema import UserInput
from nutrition_ai_backend.services.calculator_service import calculate_nutrition

app = FastAPI(title="Nutrition AI API", version="1.0.0")
BASE_DIR = Path(__file__).resolve().parent


@app.get("/")
def web_app() -> FileResponse:
    return FileResponse(BASE_DIR / "ui" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/calculate")
def calculate(user: UserInput) -> dict:
    return calculate_nutrition(user)
