from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

telemetry_data = []

class TelemetryEntry(BaseModel):
    id: str = None
    device: str
    cpu_percent: float
    mem_percent: float
    temperature_c: float
    timestamp: str = None

@router.post("/push")
def push_telemetry(entry: TelemetryEntry):
    entry.id = str(uuid.uuid4())
    entry.timestamp = datetime.utcnow().isoformat()
    telemetry_data.append(entry)
    return entry

@router.get("/latest", response_model=List[TelemetryEntry])
def latest_telemetry():
    return telemetry_data
