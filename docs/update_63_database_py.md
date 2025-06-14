📄 Quelltext:

markdown
Kopieren
Bearbeiten
# 🗄️ Update 63 – Datenbank-Engine-Vereinheitlichung (`database.py`)

## Ziel
Anpassung und Prüfung der zentralen SQLAlchemy-Session für volle Kompatibilität mit Seed-Skripten und Tests.

## Betroffene Datei
📄 `C:\noc_project\UltraNOC\backend\app\database.py`

## Änderung

### ✅ Vollständiger Inhalt

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/ultranoc")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Vorteile
✅ Sichere Datenbankbindung via .env

✅ Autocommit deaktiviert, vollständige Kontrolle über Transaktionen

🧪 Unterstützt alle bisherigen Tests und Seed-Prozesse

🔁 Re-usable get_db() für FastAPI-Dependency Injection

Hinweis
Diese Datei ist zwingend erforderlich für Authentifizierung, User-Router, Metrik-Router, Seed-Skripte und Testinfrastruktur.