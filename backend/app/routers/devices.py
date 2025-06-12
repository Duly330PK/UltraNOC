from fastapi import APIRouter

devices = {
    "r1": {"hostname": "R1", "ip": "192.168.1.1", "status": "up"},
    "sw1": {"hostname": "SW1", "ip": "192.168.1.2", "status": "up"}
}

router = APIRouter()

@router.get("/")
async def list_devices():
    return list(devices.values())
