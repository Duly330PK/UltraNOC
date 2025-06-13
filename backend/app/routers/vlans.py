from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

router = APIRouter()

vlan_store = []

class VLAN(BaseModel):
    id: str
    vlan_id: int
    name: str
    device: str
    timestamp: str

@router.post("/add", response_model=VLAN)
def add_vlan(vlan: VLAN):
    vlan.id = str(uuid.uuid4())
    vlan.timestamp = datetime.utcnow().isoformat()
    vlan_store.append(vlan)
    return vlan

@router.get("/list", response_model=List[VLAN])
def list_vlans():
    return vlan_store
