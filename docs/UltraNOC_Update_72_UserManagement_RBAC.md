📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 👥 UltraNOC – Update 72: Benutzerverwaltung & RBAC

## 📁 Betroffene Dateien
- `backend/app/models/user.py`
- `backend/app/routers/users.py`
- `backend/app/auth/auth_dependency.py`
- `backend/init.sql`
- `tests/test_auth.py`

---

## 🎯 Ziel

- Strukturierte Benutzerverwaltung
- Rollensystem für Zugriffsrechte
- Geschützter Endpunkt zur Benutzerauflistung (`/api/v1/users/`)

---

## 📄 Beispiel – User-Modell (models/user.py)

```python
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
🔐 Rollenprüfung (auth_dependency.py)
python
Kopieren
Bearbeiten
def require_role(role: str):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(status_code=403, detail="User does not have required role")
        return current_user
    return dependency
🔎 Benutzer-Endpunkt (nur für Admins)
http
Kopieren
Bearbeiten
GET /api/v1/users/
Authorization: Bearer <token>
Antwort:

json
Kopieren
Bearbeiten
[
  {
    "username": "admin",
    "role": "admin"
  }
]
🧪 Testfälle
Login mit admin

Zugriff auf /users/ mit gültigem Token

Fehler bei Rolle ≠ admin

✅ Ergebnisse
Feature	Status
RBAC umgesetzt	✅
Benutzer-Endpunkt geschützt	✅
Tokenprüfung erfolgreich	✅
Admin vs. Nicht-Admin geprüft	✅

© 2025 UltraNOC – Benutzer- & Rechtemanagement auf NOC-Niveau