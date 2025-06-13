from fastapi import APIRouter
from typing import Dict
import json
import os

router = APIRouter()

PREVIEW_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "topology_preview.json")
)

@router.get("/preview")
def get_preview():
    if os.path.exists(PREVIEW_FILE):
        with open(PREVIEW_FILE) as f:
            return json.load(f)
    return {"error": "No preview found"}

@router.post("/preview")
def set_preview(data: Dict):
    os.makedirs(os.path.dirname(PREVIEW_FILE), exist_ok=True)
    with open(PREVIEW_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "saved"}
