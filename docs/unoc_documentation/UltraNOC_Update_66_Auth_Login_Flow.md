📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Update 66: Authentifizierungs-Flow (Login, Token, Rollen)

## 📁 Pfad
C:\noc_project\UltraNOC\docs\UltraNOC_Update_66_Auth_Login_Flow.md

---

## 🧩 Ziel
Produktionsnahe Authentifizierung mit:

- Login-Endpunkt (OAuth2 + JWT)
- Passwortprüfung mit `bcrypt`
- Rollenbasiertem Zugriff (admin, user)
- Token-geschützten Routen
- User-Listing nur für Admins

---

## 📌 Beteiligte Dateien

| Datei                                                      | Änderungstyp | Funktion                              |
|------------------------------------------------------------|--------------|---------------------------------------|
| backend\app\routers\auth_router.py                         | 🆕 Login     | POST /api/v1/auth/login               |
| backend\app\auth\token_handler.py                          | 🔁 Geändert  | JWT-Token mit UTC                    |
| backend\app\models\user.py                                 | 🔁 Geändert  | hashed_password + Role                |
| backend\app\schemas\auth_schemas.py                        | 🆕 Schemas   | LoginRequest + TokenResponse          |
| backend\app\auth\auth_dependency.py                        | 🆕 NEU       | `get_current_user` + `require_role`   |
| backend\app\routers\users.py                               | 🆕 NEU       | /users (GET) nur für Admin            |
| backend\app\main.py                                        | 🔁 Router    | Einbindung aller Komponenten          |
| backend\tests\test_auth.py                                 | 🆕 Test      | Login-Validierung                     |
| scripts\init_users.sql                                     | 🆕 Seed      | Admin-Nutzer + bcrypt-hash            |

---

## 🔑 POST /api/v1/auth/login

Form-Daten (x-www-form-urlencoded):
- `username`: admin
- `password`: geheim123

### Response
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
🔒 GET /api/v1/users/
Header:
Authorization: Bearer <jwt_token>

Nur mit gültigem Token UND Rolle = admin.

json
Kopieren
Bearbeiten
[
  {
    "username": "admin",
    "role": "admin"
  }
]
🔧 Details zur Implementierung
Passwortvergleich: passlib.context.CryptContext(bcrypt)

Token mit Ablauf: exp = now(timezone.utc) + timedelta(...)

Auth-Schutz: Depends(require_role("admin"))

JWT-Verarbeitung: sub enthält username

⚙️ .env Parameter (Beispiel)
ini
Kopieren
Bearbeiten
SECRET_KEY=ultranoc-secret
DATABASE_URL=postgresql://root:root@localhost/ultranoc
✅ Testabdeckung
test_auth.py prüft: Login-Statuscode + Feldvalidierung

Test der Rolle und Zugriffssperre erfolgt implizit über Route /users

📊 Vorteile
Feature	Status
Hash-Vergleich	✅
Rollenprüfung	✅
Token-Blacklist	❌ geplant
Token-Refresh	❌ geplant
Login-UI-Anbindung	🔜

⏭️ Ausblick
Frontend-Anbindung (Login, Token speichern)

Refresh-Token-Modul (Update 67)

Password Reset + User Management API

