from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()
logs = []

class SyslogEntry(BaseModel):
    source: str
    severity: str
    message: str

@router.post("/send")
def receive_log(entry: SyslogEntry):
    log_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "source": entry.source,
        "severity": entry.severity,
        "message": entry.message
    }
    logs.append(log_entry)
    return log_entry

@router.get("/all")
def get_logs():
    return logs
