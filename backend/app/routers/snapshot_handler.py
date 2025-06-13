from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import os
import json

router = APIRouter()

SNAPSHOT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "config_snapshots.json"))

class Snapshot(BaseModel):
    device: str
    config: str

@router.post("/save")
def save_snapshot(snap: Snapshot):
    os.makedirs(os.path.dirname(SNAPSHOT_FILE), exist_ok=True)
    try:
        with open(SNAPSHOT_FILE) as f:
            data = json.load(f)
    except:
        data = []

    entry = {
        "device": snap.device,
        "config": snap.config,
        "timestamp": datetime.utcnow().isoformat()
    }
    data.append(entry)

    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return {"status": "saved", "device": snap.device}

@router.get("/list")
def get_snapshots():
    if os.path.exists(SNAPSHOT_FILE):
        with open(SNAPSHOT_FILE) as f:
            return json.load(f)
    return []
