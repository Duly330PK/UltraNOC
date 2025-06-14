📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Update 78: Authentifizierungsschemas für Login & Token

## 📁 Datei

- `backend/app/schemas/auth_schemas.py`

---

## 📦 Inhalt

### ✅ LoginRequest

```python
class LoginRequest(BaseModel):
    username: str
    password: str
Verwendet für alternative Authentifizierungs-Endpunkte (z. B. POST via REST-Client statt OAuth2PasswordRequestForm).

✅ TokenResponse
python
Kopieren
Bearbeiten
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
Wird bei erfolgreicher Anmeldung zurückgegeben. Kompatibel mit OAuth2-Flow.

🧩 Vorteile
Entkopplung der Eingabevalidierung von FastAPI-internen Security-Modulen.

Frontend-kompatibel, insbesondere für React/JS-Clients.

Ermöglicht strukturierte Tests über pytest und REST-Tools.

🔄 Abhängigkeiten
Wird importiert von:

auth_router.py (POST /auth/login)

token_handler.py (TokenResponse)

ggf. zukünftigen Routen wie POST /auth/refresh

✅ Status
Schema	Typ	Zweck	Einsatzbereit
LoginRequest	Eingabe	Benutzeranmeldung	✅
TokenResponse	Ausgabe	JWT-Rückgabe	✅

© 2025 UltraNOC – Einheitliche Authentifizierungsdaten für Backend & Clients