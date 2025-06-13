from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel
import json
import os

router = APIRouter()

MAINTENANCE_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "maintenance_schedule.json")
)

class ScheduleEntry(BaseModel):
    id: str
    description: str
    start_time: str
    end_time: str

@router.post("/schedule")
def add_schedule(entry: ScheduleEntry):
    os.makedirs(os.path.dirname(MAINTENANCE_FILE), exist_ok=True)
    try:
        with open(MAINTENANCE_FILE) as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry.dict())
    with open(MAINTENANCE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "added", "entries": len(data)}

@router.get("/schedule")
def get_schedule():
    if os.path.exists(MAINTENANCE_FILE):
        with open(MAINTENANCE_FILE) as f:
            return json.load(f)
    return []
