📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Update 71: Authentifizierung (Login-Endpunkt)

## 📁 Betroffene Dateien
- `backend/app/routers/auth_router.py`
- `backend/app/models/user.py`
- `backend/app/schemas/auth_schemas.py`
- `backend/app/auth/token_handler.py`
- `backend/init.sql`

---

## ✅ Ziel

Ein produktionsreifer Authentifizierungsmechanismus auf Basis von JWT-Tokens.  
Der Login erfolgt über `/api/v1/auth/login` mittels `OAuth2PasswordRequestForm`.

---

## 🔑 Ablauf

1. Nutzer sendet Login-Formular (`username`, `password`)
2. Server verifiziert Passwort-Hash (bcrypt)
3. Bei Erfolg: JWT wird generiert und zurückgegeben
4. Token kann für geschützte Endpunkte genutzt werden

---

## 📄 Beispiel-Request (HTTP-Client)

POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=test123

css
Kopieren
Bearbeiten

**Antwort:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer"
}
⚙️ Token-Erzeugung
python
Kopieren
Bearbeiten
expire = datetime.now(timezone.utc) + timedelta(minutes=60)
jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm="HS256")
UTC-Zeit wird verwendet

.env-basierter SECRET_KEY unterstützt

Token läuft nach definierter Zeit ab

🧪 Tests
Test in tests/test_auth.py prüft:

Erfolgreiche Anmeldung

Fehlerhafte Credentials

Struktur des Token-Response

🔐 Sicherheit & Hinweise
Komponente	Status
Passwort-Hashing (bcrypt)	✅ aktiv
SQLAlchemy-Zugriff	✅ integriert
.env-Integration	✅ vorhanden
Role-Based Access	🔜 folgt

© 2025 UltraNOC – Sichere Authentifizierung für NOC-Systeme