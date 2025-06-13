from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

device_health_data = []

class DeviceHealth(BaseModel):
    id: str = None
    device: str
    cpu_usage: float
    memory_usage: float
    timestamp: str = None

@router.post("/report")
def report_health(entry: DeviceHealth):
    entry.id = str(uuid.uuid4())
    entry.timestamp = datetime.utcnow().isoformat()
    device_health_data.append(entry)
    return entry

@router.get("/latest", response_model=List[DeviceHealth])
def get_latest():
    return device_health_data
