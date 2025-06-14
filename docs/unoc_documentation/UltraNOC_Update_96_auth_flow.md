📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Authentifizierungs- und Login-Flow

## 📌 Ziel
Implementierung eines vollständigen Login-Mechanismus mit Benutzerprüfung, JWT-Tokenvergabe und Rollenprüfung.

---

## 🧩 Bestandteile

| Datei | Beschreibung |
|-------|--------------|
| `routers/auth_router.py` | POST /login – Login-Endpunkt |
| `auth/token_handler.py` | Token-Generierung (JWT) |
| `schemas/auth_schemas.py` | LoginRequest, TokenResponse |
| `models/user.py` | SQLAlchemy-Modell mit UUID, Role |
| `tests/test_auth.py` | Unit-Test für Login |

---

## 🔐 Authentifizierung

**Login-Aufruf:**

- **Pfad:** `POST /api/v1/auth/login`
- **Formdaten:** `username`, `password`
- **Antwort:** `access_token`, `token_type`

**Beispiel:**
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
🧾 JWT Token-Erzeugung
Algorithmus: HS256

Ablauf: 60 Minuten

UTC-konform:

python
Kopieren
Bearbeiten
expire = datetime.now(timezone.utc) + timedelta(...)
👥 Benutzerliste (geschützt)
Pfad: GET /api/v1/users/

Header: Authorization: Bearer <TOKEN>

Berechtigung: nur role=admin

✅ Sicherheitsmechanismen
Funktion	Umsetzung
Passwort-Hash	bcrypt (passlib)
Token-Verfall	60 min, UTC-Zeit
Rollenprüfung	require_role("admin")
Schutzfilter	OAuth2PasswordBearer

📦 Zusammenfassung
Feature	Status
Login (POST /login)	✅
Token-Logik (JWT)	✅
Rollenbasierte API	✅
Seed-Nutzer nutzbar	✅
.env-Unterstützung	✅

© 2025 UltraNOC – Authentifizierungsmodul (Update 61–62)