from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
import uuid

router = APIRouter()

snapshots = {}

class Snapshot(BaseModel):
    id: str = None
    timestamp: str = None
    content: Dict

@router.post("/save")
def save_snapshot(snapshot: Snapshot):
    snapshot.id = str(uuid.uuid4())
    snapshot.timestamp = datetime.utcnow().isoformat()
    snapshots[snapshot.id] = snapshot
    return snapshot

@router.get("/load/{snapshot_id}")
def load_snapshot(snapshot_id: str):
    return snapshots.get(snapshot_id, {})
