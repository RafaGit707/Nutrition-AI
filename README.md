# Nutrition AI (Monorepo: Backend + Frontend)

Proyecto web escalable para cálculo nutricional, pensado para evolucionar a IA adaptativa con datos reales.

## Estructura

- `nutrition_ai_backend/` -> API FastAPI + motor nutricional
- `nutrition_ai_frontend/` -> frontend web (vanilla JS, desacoplado por API)

## Backend (FastAPI)

### Qué hace
- valida perfil de usuario (variables obligatorias + extras)
- calcula BMR (Mifflin-St Jeor)
- calcula TDEE con actividad + ajustes de contexto
- ajusta calorías por objetivo (`bulk`, `maintenance`, `cut`)
- calcula macros y notas de coaching

### Endpoints
- `GET /` -> UI de prueba del backend
- `GET /health` -> estado
- `POST /calculate` -> cálculo nutricional

### Ejecutar backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn nutrition_ai_backend.main:app --reload
```

Swagger:
- `http://127.0.0.1:8000/docs`

## Frontend

Frontend independiente consumiendo `POST /calculate`.

### Ejecutar frontend (rápido)
```bash
python -m http.server 4173 --directory nutrition_ai_frontend
```

Abrir:
- `http://127.0.0.1:4173/`

> El frontend usa por defecto `http://127.0.0.1:8000` como API.

## Variables implementadas
- Edad
- Peso (kg)
- Estatura (cm)
- Género
- % grasa corporal
- Nivel de actividad diaria (NEAT)
- Días de entrenamiento
- Tipo de entrenamiento
- Experiencia entrenando (años)
- Objetivo
- Horas de sueño
- Estrés (1-5)
- Historial deportivo previo

Extras:
- Tipo corporal
- Pasos diarios medios
- Tipo de trabajo
- Factor metabólico estimado

## Nota de arquitectura
No hace falta separar repositorio todavía. Este monorepo es ideal para iterar rápido backend+frontend; cuando haya equipos y despliegues independientes, se puede dividir sin romper contratos de API.
