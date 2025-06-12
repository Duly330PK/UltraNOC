from fastapi import APIRouter
from app.simulation import cables, routing
from app.routers import devices

router = APIRouter()

@router.get("/devices")
async def get_all_devices():
    return list(devices.devices.values())

@router.get("/links")
async def get_all_links():
    return cables.list_fiber_links()

@router.get("/routing/{device_id}")
async def get_routing_table(device_id: str):
    return routing.get_routing_table(device_id)
