from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

router = APIRouter()
port_map = []

class PortEntry(BaseModel):
    device: str
    port: str
    description: str

@router.post("/map")
def map_port(entry: PortEntry):
    record = {
        "id": str(uuid.uuid4()),
        "device": entry.device,
        "port": entry.port,
        "description": entry.description,
        "timestamp": datetime.utcnow().isoformat()
    }
    port_map.append(record)
    return record

@router.get("/map")
def get_ports():
    return port_map
