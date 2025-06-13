from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()

cgnat_pools = []

class CGNATEntry(BaseModel):
    id: str = None
    public_ip: str
    port_range: str

@router.post("/add")
def add_pool(entry: CGNATEntry):
    entry.id = str(uuid.uuid4())
    cgnat_pools.append(entry)
    return entry

@router.get("/list", response_model=List[CGNATEntry])
def list_pools():
    return cgnat_pools
