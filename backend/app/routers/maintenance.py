from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

status = {"mode": "normal", "since": datetime.utcnow().isoformat()}

class MaintenanceToggle(BaseModel):
    mode: str  # "normal", "maintenance"

@router.post("/set")
def set_mode(toggle: MaintenanceToggle):
    status["mode"] = toggle.mode
    status["since"] = datetime.utcnow().isoformat()
    return status

@router.get("/status")
def get_mode():
    return status
