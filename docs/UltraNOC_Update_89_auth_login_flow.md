📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Authentifizierungsmodul (Login Flow)

## 📌 Ziel
Ein produktionsnaher Login-Prozess über OAuth2-kompatibles Token-Verfahren, inklusive Nutzerverifikation, Passwortprüfung (bcrypt) und sicherer JWT-Erzeugung.

---

## 🧱 Komponenten

| Datei | Zweck |
|-------|-------|
| `routers/auth_router.py` | Endpunkt für Login (`/api/v1/auth/login`) |
| `auth/token_handler.py` | Token-Logik (JWT-Erstellung) |
| `schemas/auth_schemas.py` | Pydantic-Schema: LoginRequest, TokenResponse |
| `models/user.py` | Datenbankmodell mit `username`, `hashed_password`, `role` |

---

## 🔁 Login-Endpunkt

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin
🔄 Antwort (200 OK):
json
Kopieren
Bearbeiten
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
🔐 Fehlerfall (401 Unauthorized):
json
Kopieren
Bearbeiten
{
  "detail": "Invalid credentials"
}
🔧 TokenHandler – JWT-Erzeugung
python
Kopieren
Bearbeiten
def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
✅ Sicherheit & Best Practices
bcrypt zur Passwortprüfung

Token mit Ablaufzeit & Signierung

Zugriff über OAuth2-Form → kompatibel mit Swagger UI

Token-Erstellung nutzt .env (SECRET_KEY)

🔄 Pydantic-Schemas
python
Kopieren
Bearbeiten
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
🧪 Testbeispiel
python
Kopieren
Bearbeiten
def test_login_success():
    response = client.post("/api/v1/auth/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()
© 2025 UltraNOC – Authentifizierungsmodul Dokumentation (Stand: Update 62)