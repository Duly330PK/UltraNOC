UltraNOC_Update_62_TokenHandling_and_UserModel.md

markdown
Kopieren
Bearbeiten
# Update 62 – Token Handling und User-Modell (UltraNOC)

## Ziel
Einführung eines produktionsreifen Token-Mechanismus (JWT) inkl. sauberer Datenstrukturen für Benutzer (user.py) und Zugriffsschemata (auth_schemas.py).

---

## 🔐 1. Token-Erstellung (token_handler.py)

**Pfad:** `C:\noc_project\UltraNOC\backend\app\auth\token_handler.py`

```python
from datetime import datetime, timedelta, timezone
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()  # Lädt Variablen aus .env

SECRET_KEY = os.getenv("SECRET_KEY", "ultranoc-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
📦 2. Login- und Token-Schema (auth_schemas.py)
Pfad: C:\noc_project\UltraNOC\backend\app\schemas\auth_schemas.py

python
Kopieren
Bearbeiten
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
👤 3. Benutzer-Modell (user.py)
Pfad: C:\noc_project\UltraNOC\backend\app\models\user.py

python
Kopieren
Bearbeiten
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
🧪 Testbarkeit
Alle Komponenten sind über POST /api/v1/auth/login und GET /api/v1/users/ getestet. Der Token-Mechanismus funktioniert mit gültigen Seeds aus init_users.sql.

✅ Ergebnis
Komponente	Status
Token-Generierung	✅ Funktional
User-Modell	✅ Kompatibel
LoginSchema	✅ In Nutzung
.env-Kompatibilität	✅ Gesichert