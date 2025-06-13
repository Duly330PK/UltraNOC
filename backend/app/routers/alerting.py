from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

alerts = []

class Alert(BaseModel):
    id: str = None
    source: str
    level: str
    message: str
    timestamp: str = None

@router.post("/raise", response_model=Alert)
def raise_alert(alert: Alert):
    alert.id = str(uuid.uuid4())
    alert.timestamp = datetime.utcnow().isoformat()
    alerts.append(alert)
    return alert

@router.get("/all", response_model=List[Alert])
def get_all_alerts():
    return alerts
