from fastapi import APIRouter
import socket
import platform
import psutil
from datetime import datetime

router = APIRouter()

@router.get("/probe")
def probe():
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "uptime": datetime.utcnow().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": dict(psutil.virtual_memory()._asdict())
    }
