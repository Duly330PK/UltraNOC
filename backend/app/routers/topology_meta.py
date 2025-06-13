from fastapi import APIRouter
import json
import os

router = APIRouter()

TOPO_FILE = "data/topology_metadata.json"

@router.get("/meta")
def get_topology_metadata():
    if os.path.exists(TOPO_FILE):
        with open(TOPO_FILE, "r") as f:
            return json.load(f)
    return {"error": "topology metadata not found"}

@router.post("/meta")
def save_topology_metadata(data: dict):
    os.makedirs(os.path.dirname(TOPO_FILE), exist_ok=True)  # ← das hinzufügen
    with open(TOPO_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "saved"}


