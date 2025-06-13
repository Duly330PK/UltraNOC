from fastapi import APIRouter
import random
from datetime import datetime

router = APIRouter()

@router.get("/services")
def get_service_status():
    services = {
        "db": random.choice(["running", "stopped", "degraded"]),
        "api": "running",
        "cli": "running",
        "frontend": "running",
    }
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "services": services
    }
