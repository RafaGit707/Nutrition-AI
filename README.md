# Nutrition AI (Monorepo: Backend + Frontend)

Proyecto web escalable para cálculo nutricional, pensado para evolucionar a IA adaptativa con datos reales.

## Estructura corregida (entrypoint listo para deploy)

```text
.
├── main.py                       # Entrypoint FastAPI para deploy -> main:app
├── requirements.txt
├── nutrition_ai_backend/
│   ├── main.py                   # Compat wrapper que reexporta app
│   ├── schemas/
│   ├── models/
│   ├── services/
│   ├── future_ml/
│   └── ui/
└── nutrition_ai_frontend/
    ├── index.html
    └── src/
```

## ¿Por qué aparece "No fastapi entrypoint found"?

Suele pasar cuando la plataforma no encuentra una variable global `app` en el módulo indicado por el start command.
Ejemplo: si Render usa `main:app` pero `main.py` no define `app = FastAPI()`, el deploy falla.

En este proyecto se corrige creando `main.py` en raíz con:
- `from fastapi import FastAPI`
- `app = FastAPI(...)`
- endpoints básicos (`/health`, `/`, `/calculate`)

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

### Ejecutar local con uvicorn (recomendado)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
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

## Render.com

### Start Command (ejemplo correcto)
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### requirements.txt (ejemplo mínimo)
```txt
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.8.0
```

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
