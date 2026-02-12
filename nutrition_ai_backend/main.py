from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from nutrition_ai_backend.schemas.user_schema import UserInput
from nutrition_ai_backend.services.calculator_service import calculate_nutrition

app = FastAPI(title="Nutrition AI API", version="1.1.0")
BASE_DIR = Path(__file__).resolve().parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:4173",
        "http://localhost:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def web_app() -> FileResponse:
    return FileResponse(BASE_DIR / "ui" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/calculate")
def calculate(user: UserInput) -> dict:
    return calculate_nutrition(user)
