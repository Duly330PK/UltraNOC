import os
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Warten auf die Datenbank, um Race Conditions beim ersten Start im Docker-Compose zu vermeiden
print("Warte 5 Sekunden auf die Datenbank...")
time.sleep(5)

# Füge das 'app'-Verzeichnis zum Python-Pfad hinzu, damit die Module gefunden werden
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.database import Base
from app.models.user import User
from app.models.cgnat_log import CGNATLog
from app.models.security_event import Incident, SecurityEvent
from app.auth.auth_handler import get_password_hash

load_dotenv()

# Verwende die DATABASE_URL aus den Umgebungsvariablen, die von Docker Compose gesetzt wird
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL ist nicht gesetzt. Stelle sicher, dass die Umgebungsvariable korrekt übergeben wird.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_db_connection():
    retries = 5
    while retries > 0:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Datenbankverbindung erfolgreich hergestellt.")
            return True
        except Exception as e:
            print(f"Warte auf Datenbank... verbleibende Versuche: {retries-1}. Fehler: {e}")
            retries -= 1
            time.sleep(5)
    return False

def initialize_database():
    if not check_db_connection():
        print("Konnte keine Verbindung zur Datenbank herstellen. Abbruch.")
        return

    print("Initialisiere Datenbank-Tabellen...")
    try:
        # Erstelle alle Tabellen, die von `Base` erben
        Base.metadata.create_all(bind=engine)
        print("Tabellen erfolgreich erstellt.")
    except Exception as e:
        print(f"Fehler beim Erstellen der Tabellen: {e}")
        return

    db = SessionLocal()
    try:
        # Füge den Admin-Benutzer hinzu, falls er noch nicht existiert
        if not db.query(User).filter(User.username == "admin").first():
            print("Admin-Benutzer wird erstellt...")
            hashed_password = get_password_hash("admin123")
            admin = User(username="admin", hashed_password=hashed_password, role="admin")
            db.add(admin)
            db.commit()
            print("Admin-Benutzer 'admin' mit Passwort 'admin123' erstellt.")
        else:
            print("Admin-Benutzer existiert bereits.")
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database()