import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Lädt die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Holt die Datenbank-URL aus der Umgebungsvariable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Erstellt die SQLAlchemy-Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session-Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency für FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
