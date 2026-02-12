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
- Objetivo (bulk / maintenance / cut)
- Horas de sueño
- Estrés (1-5)
- Historial deportivo previo

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
