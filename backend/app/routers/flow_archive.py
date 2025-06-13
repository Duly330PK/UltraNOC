from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid
import os
import json

router = APIRouter()

ARCHIVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/flow_archive.json"))
flow_entries = []

class FlowRecord(BaseModel):
    id: str = None
    src: str
    dst: str
    bandwidth_mbps: float
    duration_s: int
    timestamp: str = None

def save_to_file():
    os.makedirs(os.path.dirname(ARCHIVE_PATH), exist_ok=True)
    with open(ARCHIVE_PATH, "w") as f:
        json.dump([entry.dict() for entry in flow_entries], f, indent=2)

@router.post("/add", response_model=FlowRecord)
def add_flow(record: FlowRecord):
    record.id = str(uuid.uuid4())
    record.timestamp = datetime.utcnow().isoformat()
    flow_entries.append(record)
    save_to_file()
    return record

@router.get("/list", response_model=List[FlowRecord])
def list_flows():
    return flow_entries

@router.get("/flows")
def get_flows():
    if not os.path.exists(ARCHIVE_PATH):
        return []
    with open(ARCHIVE_PATH, "r") as f:
        return json.load(f)
