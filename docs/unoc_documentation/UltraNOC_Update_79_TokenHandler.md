📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Update 79: JWT-Erstellung in token_handler.py

## 📁 Datei

- `backend/app/auth/token_handler.py`

---

## 🧩 Funktion: `create_access_token(data: dict)`

```python
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
🔐 Geheimnisbehandlung
python
Kopieren
Bearbeiten
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "ultranoc-secret")
Ermöglicht projektspezifischen geheimen Schlüssel über .env

Fallback auf "ultranoc-secret" bei Entwicklungsumgebungen

⚙️ Konfigurationen
python
Kopieren
Bearbeiten
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
Aktuell statisch, aber .env-kompatibel anpassbar

Optional: Refresh-Token-Handling in späterem Update

📦 Abhängigkeiten
Modul	Verwendung
jose.jwt	Token-Encode/Decode
os + dotenv	Laden von Umgebungsvariablen
datetime	UTC-Token-Gültigkeitszeitpunkt

✅ Status
Aspekt	Status
Token signieren	✅
UTC-kompatible Ablaufzeit	✅
.env-Support für Secret	✅
Refresh-Token	⏳ geplant

© 2025 UltraNOC – Sichere Authentifizierungsmechanik mit JWT nach Industriestandard