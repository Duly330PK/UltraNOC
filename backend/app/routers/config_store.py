# C:\noc_project\UltraNOC\backend\app\routers\config_store.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter(prefix="/api/v1/config", tags=["Config Store"])

CONFIG_PATH = "data/config_store.json"

# Datenmodell für gespeicherte Konfiguration
class ConfigEntry(BaseModel):
    device_id: str
    config_data: str

@router.post("/store")
def store_config(entry: ConfigEntry):
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[entry.device_id] = entry.config_data

    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

    return {"status": "saved", "device_id": entry.device_id}

@router.get("/load/{device_id}")
def load_config(device_id: str):
    if not os.path.exists(CONFIG_PATH):
        raise HTTPException(status_code=404, detail="No config data found")

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    if device_id not in data:
        raise HTTPException(status_code=404, detail="Device config not found")

    return {"device_id": device_id, "config_data": data[device_id]}
