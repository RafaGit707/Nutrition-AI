import streamlit as st

from src.nutrition_ai import NutritionRegressor, UserProfile, recommendation_notes

st.set_page_config(page_title="Nutrition AI", page_icon="🥗", layout="centered")


@st.cache_resource
def get_model() -> NutritionRegressor:
    model = NutritionRegressor()
    model.fit()
    return model


st.title("🥗 Nutrition AI - Calculadora inteligente")
st.write(
    "Prototipo inicial con red neuronal para estimar calorías y macronutrientes según tus objetivos."
)

with st.form("profile_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Edad", 18, 65, 30)
        weight = st.number_input("Peso (kg)", min_value=35.0, max_value=220.0, value=75.0)
        height = st.number_input("Altura (cm)", min_value=130.0, max_value=230.0, value=175.0)
        gender = st.selectbox("Género", ["hombre", "mujer"])
        goal = st.selectbox("Objetivo", ["definicion", "mantenimiento", "volumen"])

    with col2:
        activity = st.selectbox(
            "Actividad diaria",
            ["sedentario", "ligero", "moderado", "alto", "atleta"],
            index=2,
        )
        sleep = st.slider("Horas de sueño promedio", 4.0, 10.0, 7.0, step=0.25)
        experience = st.slider("Años haciendo deporte", 0.0, 30.0, 2.0, step=0.5)
        body_fat = st.slider("Grasa corporal estimada (%)", 5.0, 45.0, 20.0, step=0.5)
        stress = st.slider("Estrés promedio (1 bajo - 5 alto)", 1, 5, 3)

    submitted = st.form_submit_button("Calcular plan")

if submitted:
    profile = UserProfile(
        age=age,
        weight_kg=weight,
        height_cm=height,
        gender=gender,
        goal=goal,
        activity_level=activity,
        sleep_hours=sleep,
        sports_experience_years=experience,
        body_fat_pct=body_fat,
        stress_level=stress,
    )

    model = get_model()
    prediction = model.predict(profile)

    st.subheader("Resultado recomendado")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calorías", f"{prediction['calories']} kcal")
    c2.metric("Proteínas", f"{prediction['protein_g']} g")
    c3.metric("Grasas", f"{prediction['fat_g']} g")
    c4.metric("Carbohidratos", f"{prediction['carbs_g']} g")

    st.subheader("Sugerencias")
    for note in recommendation_notes(profile, prediction):
        st.write(f"- {note}")

st.caption(
    "⚠️ Esta herramienta es educativa y no sustituye la valoración de un nutricionista clínico."
)
