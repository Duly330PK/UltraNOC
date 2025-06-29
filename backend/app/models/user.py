from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="Eindeutige ID des Benutzers")
    username = Column(String(100), unique=True, index=True, nullable=False, comment="Benutzername für den Login")
    hashed_password = Column(String(255), nullable=False, comment="BCrypt-gehashtes Passwort")
    role = Column(String(50), default="user", nullable=False, comment="Benutzerrolle (z.B. admin, operator, viewer)")