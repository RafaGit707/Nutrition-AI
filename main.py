"""Render/FastAPI entrypoint en raíz: `main:app`."""
"""Render/FastAPI entrypoint.

Este archivo existe en la raíz para que plataformas como Render detecten
fácilmente `main:app` sin depender de rutas internas.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from nutrition_ai_backend.schemas.user_schema import UserInput
from nutrition_ai_backend.services.calculator_service import calculate_nutrition

app = FastAPI(title="Nutrition AI API", version="1.2.1")
BACKEND_DIR = Path(__file__).resolve().parent / "nutrition_ai_backend"

# Instancia principal de FastAPI que Render/Uvicorn buscarán como `main:app`.
app = FastAPI(title="Nutrition AI API", version="1.2.0")
BACKEND_DIR = Path(__file__).resolve().parent / "nutrition_ai_backend"

# CORS para desarrollo local de frontend.
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


# Endpoint simple para verificar que el servicio responde.
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# UI simple alojada en backend para prueba rápida.
@app.get("/")
def web_app() -> FileResponse:
    return FileResponse(BACKEND_DIR / "ui" / "index.html")


# Endpoint principal de cálculo nutricional.
@app.post("/calculate")
def calculate(user: UserInput) -> dict:
    return calculate_nutrition(user)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
import uvicorn


if __name__ == "__main__":
    uvicorn.run("nutrition_ai_backend.main:app", host="127.0.0.1", port=8000, reload=True)
