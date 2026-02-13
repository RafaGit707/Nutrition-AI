# Nutrition AI (Monorepo: Backend + Frontend)

Proyecto web escalable para cálculo nutricional, pensado para evolucionar a IA adaptativa con datos reales.

## Estructura corregida (entrypoint listo para deploy)

```text
.
├── main.py
├── requirements.txt
├── nutrition_ai_backend/
│   ├── requirements.txt          # Dependencias para deploy del backend por subcarpeta
│   ├── main.py
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
    ├── requirements.txt          # Placeholder (frontend estático)
    ├── vercel.json               # Config de despliegue estático en Vercel
    ├── index.html
    └── src/
```

## Deploy por subcarpetas (Render + Vercel)

### Backend en Render (Root Directory = `nutrition_ai_backend`)

- Build Command:
  ```bash
  pip install -r requirements.txt
  ```
- Start Command:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

> `nutrition_ai_backend/main.py` también define `app` para que Render funcione si el root es esa subcarpeta.

### Frontend en Vercel (Root Directory = `nutrition_ai_frontend`)

- Framework preset: **Other** (estático)
- Build command: *(vacío)*
- Output directory: *(vacío, sirve estático directo)*
- `vercel.json` ya incluido para servir `index.html`.

## ¿Por qué aparece "No fastapi entrypoint found"?

Suele pasar cuando la plataforma no encuentra una variable global `app` en el módulo indicado por el start command.
Ejemplo: si Render usa `main:app` pero ese `main.py` no define `app = FastAPI()`, el deploy falla.

## Ejecutar local

### Backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
## ¿Por qué aparece "No fastapi entrypoint found"?

Suele pasar cuando la plataforma no encuentra una variable global `app` en el módulo indicado por el start command.
Ejemplo: si Render usa `main:app` pero `main.py` no define `app = FastAPI()`, el deploy falla.

En este proyecto se corrige creando `main.py` en raíz con:
- `from fastapi import FastAPI`
- `app = FastAPI(...)`
- endpoints básicos (`/health`, `/`, `/calculate`)
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

### Ejecutar local con uvicorn (recomendado)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
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

## requirements.txt (referencia)

Raíz y backend usan:
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
# Nutrition AI Backend (Web, escalable)

Arquitectura web inicial en **FastAPI** preparada para crecer a una IA adaptativa real.

## Objetivo actual
Calcular para cada usuario:
- calorías objetivo
- macronutrientes (proteínas, grasas, carbohidratos)
- notas de coaching iniciales

## Arquitectura (Fase 1)

1. **Capa de datos (User Profile)**
   - `nutrition_ai_backend/schemas/user_schema.py`
2. **Motor de cálculo (Nutrition Engine)**
   - `nutrition_ai_backend/models/nutrition_engine.py`
   - `nutrition_ai_backend/services/calculator_service.py`
3. **Interfaz web (GUI básica)**
   - `nutrition_ai_backend/ui/index.html`
   - endpoint raíz `/`

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
- Objetivo (bulk / maintenance / cut)
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
Extras pro:
- Tipo corporal estimado
- Pasos diarios medios
- Tipo de trabajo (sedentario/activo/físico)
- Factor metabólico estimado

## Base científica aplicada
- **BMR** por Mifflin-St Jeor.
- **TDEE** con multiplicadores de actividad (1.2 a 1.9).
- Ajustes por NEAT, sueño, estrés, experiencia, entrenamiento y contexto laboral.
- Ajuste por objetivo:
  - bulk: +10% a +20%
  - maintenance: 0%
  - cut: -15% a -25%
- Macros base:
  - proteína según objetivo/tipo de entrenamiento
  - grasas por kg
  - carbohidratos = calorías restantes

## Endpoints
- `GET /` -> GUI web simple (HTML)
- `GET /health` -> estado del servicio
- `POST /calculate` -> cálculo nutricional
# Nutrition AI (MVP)

MVP en Python con una **red neuronal (MLP)** + interfaz **Streamlit** para estimar:
- calorías diarias
- proteínas
- grasas
- carbohidratos

según objetivo (`volumen`, `mantenimiento`, `definicion`) y variables personales.

## Variables consideradas
- Edad
- Peso
- Altura
- Género
- Objetivo
- Nivel de actividad
- Horas de sueño
- Años de experiencia deportiva
- % de grasa corporal estimado
- Nivel de estrés

## Arquitectura
- `src/nutrition_ai/model.py`: crea dataset sintético + fórmula base nutricional + entrena un `MLPRegressor` multi-salida.
- `src/nutrition_ai/recommendation.py`: recomendaciones cualitativas según perfil.
- `app.py`: interfaz web en Streamlit.

El diseño está pensado para crecer: se puede reemplazar el dataset sintético por datos reales sin tocar la UI.

## Ejecutar
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn nutrition_ai_backend.main:app --reload
```

Abrir:
- Web UI: `http://127.0.0.1:8000/`
- Swagger: `http://127.0.0.1:8000/docs`

## Futuro ML
`nutrition_ai_backend/future_ml/model.py` queda como módulo reservado para:
- predicción de progreso
- ajuste semanal automático
- aprendizaje por respuesta real del usuario
streamlit run app.py
```

## Próximos pasos sugeridos
1. Guardar histórico por usuario.
2. Añadir más objetivos (recomposición, rendimiento).
3. Integrar validaciones clínicas (tasa de pérdida/ganancia segura).
4. Reentrenar modelo con datos reales anonimizados.
