from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

logs = []

class AccessLog(BaseModel):
    id: str = None
    user: str
    endpoint: str
    timestamp: str = None

@router.post("/record")
def record_log(log: AccessLog):
    log.id = str(uuid.uuid4())
    log.timestamp = datetime.utcnow().isoformat()
    logs.append(log)
    return log

@router.get("/list", response_model=List[AccessLog])
def list_logs():
    return logs
