# CLI Macro Feature

## Features
- Erstellen von CLI-Makros über POST /macro/create
- Auflisten aller Makros über GET /macro/list
- Ausführen eines gespeicherten Makros mit POST /macro/execute/{macro_id}

## Pfade
- backend/app/routers/cli_macro.py
- backend/app/routers/cli_macro_usage.py

Stellt sicher, dass die Routen in `main.py` registriert werden:

```python
from app.routers import cli_macro, cli_macro_usage
app.include_router(cli_macro.router, prefix="/api/v1/cli", tags=["CLI Macros"])
app.include_router(cli_macro_usage.router, prefix="/api/v1/cli", tags=["CLI Execution"])
```
