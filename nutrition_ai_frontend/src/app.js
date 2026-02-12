const API_BASE = window.NUTRITION_API_BASE || 'http://127.0.0.1:8000';

const fields = [
  ['age', 'Edad', 'number', 21],
  ['weight', 'Peso (kg)', 'number', 82],
  ['height', 'Estatura (cm)', 'number', 180],
  ['gender', 'Género', 'select', 'male', ['male', 'female']],
  ['body_fat', '% Grasa corporal', 'number', 18],
  ['activity_level', 'Actividad NEAT', 'select', 'moderate', ['sedentary', 'light', 'moderate', 'high', 'very_high']],
  ['training_days', 'Días de entrenamiento', 'number', 4],
  ['training_type', 'Tipo de entrenamiento', 'select', 'hypertrophy', ['none', 'strength', 'hypertrophy', 'crossfit', 'endurance', 'mixed']],
  ['training_experience_years', 'Experiencia (años)', 'number', 2],
  ['sports_history', 'Historial deportivo', 'select', 'true', ['true', 'false']],
  ['goal', 'Objetivo', 'select', 'bulk', ['bulk', 'maintenance', 'cut']],
  ['sleep_hours', 'Sueño (horas)', 'number', 7.5],
  ['stress_level', 'Estrés (1-5)', 'number', 3],
  ['body_type', 'Tipo corporal', 'select', 'mesomorph', ['ectomorph', 'mesomorph', 'endomorph', 'unknown']],
  ['avg_daily_steps', 'Pasos diarios', 'number', 8000],
  ['work_type', 'Tipo de trabajo', 'select', 'sedentary', ['sedentary', 'active', 'physical']],
  ['metabolic_rate_factor', 'Factor metabólico', 'number', 1.0],
];

const numericFields = new Set([
  'age', 'weight', 'height', 'body_fat', 'training_days', 'training_experience_years',
  'sleep_hours', 'stress_level', 'avg_daily_steps', 'metabolic_rate_factor'
]);

function buildForm() {
  const form = document.getElementById('nutrition-form');
  fields.forEach(([key, label, type, value, options]) => {
    const wrapper = document.createElement('label');
    wrapper.innerText = label;
    let input;

    if (type === 'select') {
      input = document.createElement('select');
      options.forEach((option) => {
        const el = document.createElement('option');
        el.value = String(option);
        el.text = String(option);
        if (String(option) === String(value)) el.selected = true;
        input.appendChild(el);
      });
    } else {
      input = document.createElement('input');
      input.type = 'number';
      input.step = key.includes('hours') || key.includes('factor') || key.includes('fat') || key.includes('experience') ? '0.1' : '1';
      input.value = String(value);
    }

    input.id = key;
    wrapper.appendChild(input);
    form.appendChild(wrapper);
  });
}

function parseValue(key, value) {
  if (key === 'sports_history') return value === 'true';
  if (numericFields.has(key)) return Number(value);
  return value;
}

function payloadFromForm() {
  return fields.reduce((acc, [key]) => {
    const el = document.getElementById(key);
    acc[key] = parseValue(key, el.value);
    return acc;
  }, {});
}

async function calculate() {
  const raw = document.getElementById('raw');
  const notes = document.getElementById('notes');

  try {
    const payload = payloadFromForm();
    const response = await fetch(`${API_BASE}/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    raw.textContent = JSON.stringify(data, null, 2);

    if (!response.ok) throw new Error(data?.detail ? JSON.stringify(data.detail) : 'Error de API');

    document.getElementById('calories').textContent = `${data.targets.calories} kcal`;
    document.getElementById('protein').textContent = `${data.targets.protein_g} g`;
    document.getElementById('fats').textContent = `${data.targets.fats_g} g`;
    document.getElementById('carbs').textContent = `${data.targets.carbs_g} g`;

    notes.innerHTML = '';
    data.notes.forEach((note) => {
      const li = document.createElement('li');
      li.textContent = note;
      notes.appendChild(li);
    });
  } catch (error) {
    notes.innerHTML = '';
    const li = document.createElement('li');
    li.textContent = `Error: ${error.message}`;
    notes.appendChild(li);
  }
}

buildForm();
document.getElementById('calculate-btn').addEventListener('click', calculate);
