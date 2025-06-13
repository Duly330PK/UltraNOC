from fastapi import APIRouter
import os

router = APIRouter()

DEVICE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "devices.yml"))

@router.get("/list")
def get_inventory():
    if os.path.exists(DEVICE_FILE):
        with open(DEVICE_FILE, "r") as f:
            return {"status": "ok", "device_count": sum(1 for _ in f if _.strip().startswith("-"))}
    return {"status": "error", "message": "devices.yml not found"}
