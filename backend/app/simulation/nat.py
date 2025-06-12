from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import uuid

router = APIRouter()

nat_sessions = []

class NATSession(BaseModel):
    id: str
    internal_ip: str
    external_ip: str
    port: int
    timestamp: str

@router.get("/nat/sessions", response_model=List[NATSession])
def get_sessions():
    return nat_sessions

@router.post("/nat/sessions", response_model=NATSession)
def add_session(session: NATSession):
    session.id = str(uuid.uuid4())
    nat_sessions.append(session)
    return session
