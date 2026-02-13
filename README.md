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
```bash
python -m http.server 4173 --directory nutrition_ai_frontend
```

## requirements.txt (referencia)

Raíz y backend usan:
```txt
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.8.0
```
