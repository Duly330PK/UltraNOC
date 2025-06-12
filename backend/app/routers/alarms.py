from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_alarms():
    return [{"device": "R1", "type": "interface_down", "severity": "critical"}]
