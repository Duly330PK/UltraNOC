from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()

sessions = []

class SessionInfo(BaseModel):
    id: str
    user: str
    device: str
    start_time: str

@router.post("/create", response_model=SessionInfo)
def create_session(user: str, device: str):
    session = SessionInfo(
        id=str(uuid.uuid4()),
        user=user,
        device=device,
        start_time=datetime.utcnow().isoformat()
    )
    sessions.append(session)
    return session

@router.get("/active", response_model=List[SessionInfo])
def active_sessions():
    return sessions
