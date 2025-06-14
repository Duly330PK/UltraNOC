# Update 61 – Login-Authentifizierungsflow (Backend)

Dieses Update implementiert den vollständigen Login-Endpunkt mit OAuth2-Standardlogik, Passwortprüfung und JWT-Token-Erstellung.

## 🔐 Zielsetzung
Ein produktiver Authentifizierungs-Endpoint (`/api/v1/auth/login`), der Benutzername und Passwort prüft, einen Zugriffstoken erzeugt und ihn im Response liefert.

---

## 📁 Geänderte/Neue Dateien

### 1. `backend/app/routers/auth_router.py`
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.auth.token_handler import create_access_token
from app.schemas.auth_schemas import TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=token)
```

### 2. `backend/tests/test_auth.py`
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_valid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "wrongpass"}
    )
    assert response.status_code == 401
```

---

## ✅ Ergebnis

| Komponente         | Status  |
|--------------------|---------|
| Login via POST     | ✔       |
| Passwortprüfung    | ✔ bcrypt |
| Token-Erstellung   | ✔ JWT  |
| Testabdeckung      | ✔ vorhanden |

Der Endpunkt ist getestet und bereit für produktiven Einsatz.
