"""Compat entrypoint.

Se mantiene para compatibilidad con comandos antiguos:
`uvicorn nutrition_ai_backend.main:app --reload`

La app real vive en `main.py` (raíz) para evitar errores de deploy
como "No fastapi entrypoint found".
"""

from main import app

__all__ = ["app"]
