📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Update 67: Authentifizierungssystem V1

## 📁 Pfad
C:\noc_project\UltraNOC\docs\UltraNOC_Update_67_Auth_System.md

---

## 🎯 Ziel

Einführung eines vollwertigen Authentifizierungssystems auf Basis von JWT, rollenbasiertem Zugriff und Token-Security.

---

## 🧩 Komponentenübersicht

| Datei                                                       | Zweck                            |
|-------------------------------------------------------------|----------------------------------|
| app\routers\auth_router.py                                  | Login-Endpunkt (/auth/login)     |
| app\auth\token_handler.py                                   | Token-Erstellung, Signatur       |
| app\core\auth.py                                            | Token-Verarbeitung & Gültigkeit  |
| app\models\user.py                                          | Usermodell (username, hash, role)|
| app\schemas\auth_schemas.py                                 | LoginRequest, TokenResponse      |
| tests\test_auth.py                                          | Test für Login-Flow              |

---

## 🔑 Login-Endpunkt

### POST /api/v1/auth/login

**Form-Parameter (x-www-form-urlencoded):**

```text
username=admin
password=admin
Response (TokenResponse):

json
Kopieren
Bearbeiten
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
🔐 Token-Erzeugung (JWT)
python
Kopieren
Bearbeiten
from datetime import datetime, timedelta, timezone

def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
🧪 Test: test_auth.py
python
Kopieren
Bearbeiten
def test_login_success():
    response = client.post("/api/v1/auth/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()
🔒 Geschützter Zugriff
Beispiel – GET /api/v1/users/ (nur für Rolle admin):

bash
Kopieren
Bearbeiten
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/api/v1/users/
✅ Sicherheitsvorteile
Feature	Status
Passwort-Hash (bcrypt)	✅
Token-Verfall (60 Min)	✅
Rollenprüfung per Dependency	✅
Testbarkeit mit pytest	✅

🗂 Nächste Schritte
Refresh-Tokens

Frontend-Anbindung

Benutzerverwaltung per API

© 2025 UltraNOC – Auth API & Token Handling