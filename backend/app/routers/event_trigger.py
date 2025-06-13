from fastapi import APIRouter
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter()

events = []

class TriggerEvent(BaseModel):
    source: str
    event_type: str
    detail: str

@router.post("/trigger")
def trigger_event(event: TriggerEvent):
    record = {
        "id": str(uuid.uuid4()),
        "source": event.source,
        "event_type": event.event_type,
        "detail": event.detail,
        "timestamp": datetime.utcnow().isoformat()
    }
    events.append(record)
    return record

@router.get("/triggered")
def list_events():
    return events
