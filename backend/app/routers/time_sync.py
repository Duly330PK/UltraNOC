from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/current-time")
def get_current_time():
    return {
        "time": datetime.utcnow().isoformat(),
        "timezone": "UTC"
    }
