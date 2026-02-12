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
streamlit run app.py
```

## Próximos pasos sugeridos
1. Guardar histórico por usuario.
2. Añadir más objetivos (recomposición, rendimiento).
3. Integrar validaciones clínicas (tasa de pérdida/ganancia segura).
4. Reentrenar modelo con datos reales anonimizados.
