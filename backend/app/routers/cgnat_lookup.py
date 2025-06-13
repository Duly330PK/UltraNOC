from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()
cgnat_table = []

class NATEntry(BaseModel):
    external_ip: str
    external_port: int
    internal_ip: str
    user_id: str

@router.post("/map")
def map_nat(entry: NATEntry):
    record = {
        "id": str(uuid.uuid4()),
        "external_ip": entry.external_ip,
        "external_port": entry.external_port,
        "internal_ip": entry.internal_ip,
        "user_id": entry.user_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    cgnat_table.append(record)
    return record

@router.get("/reverse/{external_ip}")
def reverse_lookup(external_ip: str):
    return [e for e in cgnat_table if e["external_ip"] == external_ip]
