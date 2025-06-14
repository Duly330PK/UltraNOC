📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🛡️ UltraNOC – Update 64: Login-Endpunkt (JWT Authentication)

## 📁 Pfad
C:\noc_project\UltraNOC\docs\UltraNOC_Update_64_Auth_Login_API.md

---

## 🔐 Zielsetzung
Dieses Update aktiviert den produktiven Login-Prozess via:
- Datenbankbasierter Nutzerprüfung (Usermodell)
- Passwort-Hashing mit `bcrypt`
- Token-Erstellung über JWT
- Zugriffsschutz per OAuth2

---

## 📌 Beteiligte Dateien

| Datei                                                                 | Änderungstyp | Zweck                                    |
|-----------------------------------------------------------------------|--------------|------------------------------------------|
| backend\app\routers\auth_router.py                                   | ✅ Neu       | Login-Endpunkt POST /login               |
| backend\app\models\user.py                                           | 🔁 Geändert  | Sicherer Passwort-Hash & UUID            |
| backend\app\schemas\auth_schemas.py                                  | ✅ Neu       | LoginRequest & TokenResponse             |
| backend\app\auth\token_handler.py                                    | 🔁 Geändert  | Token-Erstellung, Zeitzonenkompatibel    |
| backend\tests\test_auth.py                                           | ✅ Neu       | Testet Login-Funktion mit Tokenausgabe   |

---

## 🔑 Beispielaufruf

### Request (via curl/Postman):
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
Response:
json
Kopieren
Bearbeiten
{
  "access_token": "<JWT-TOKEN>",
  "token_type": "bearer"
}
✅ Funktionstest
Login über POST funktioniert mit Seed-Nutzer admin

Passwort-Validierung über bcrypt

Token im Standardformat (Authorization: Bearer <token>)

Token kann verwendet werden für geschützte Routen wie /api/v1/users/

🔐 Sicherheit
Token basiert auf .env-basiertem SECRET_KEY

Zeitliche Gültigkeit (60 Minuten)

Kompatibel mit RBAC-Erweiterung (role: admin)

⏭️ Nächster Schritt
Absicherung weiterer API-Endpunkte durch Rollenprüfung (RBAC)