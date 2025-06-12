from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter()

# In-Memory NAT-Tabelle
nat_sessions = []

# Modell für NAT-Eintrag
class NATSession(BaseModel):
    id: str = None
    internal_ip: str
    external_ip: str
    port: int
    timestamp: str = None

# Endpunkt: Alle NAT-Sessions abrufen
@router.get("/sessions", response_model=List[NATSession])
def get_sessions():
    return nat_sessions

# Endpunkt: Neue Session hinzufügen
@router.post("/sessions", response_model=NATSession)
def add_session(session: NATSession):
    session.id = str(uuid.uuid4())
    session.timestamp = datetime.utcnow().isoformat()
    nat_sessions.append(session)
    return session
