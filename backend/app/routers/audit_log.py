from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
from typing import List
import uuid

router = APIRouter()

logs = []

class AuditEntry(BaseModel):
    id: str
    username: str
    action: str
    target: str
    timestamp: str

@router.post("/log", response_model=AuditEntry)
def log_action(entry: AuditEntry):
    entry.id = str(uuid.uuid4())
    entry.timestamp = datetime.utcnow().isoformat()
    logs.append(entry)
    return entry

@router.get("/log", response_model=List[AuditEntry])
def get_logs():
    return logs
