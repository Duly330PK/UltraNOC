from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

router = APIRouter()

interface_stats = []

class InterfaceStat(BaseModel):
    id: str = None
    device: str
    interface: str
    in_bytes: int
    out_bytes: int
    timestamp: str = None

@router.post("/report")
def report_stat(stat: InterfaceStat):
    stat.id = str(uuid.uuid4())
    stat.timestamp = datetime.utcnow().isoformat()
    interface_stats.append(stat)
    return stat

@router.get("/all", response_model=List[InterfaceStat])
def all_stats():
    return interface_stats
