# Pfad: backend/app/routers/topology_router.py

from fastapi import APIRouter
from app.routers import devices
from app.simulation import cables, redundancy

router = APIRouter()

@router.get("/devices")
async def get_all_devices():
    return list(devices.devices.values())

@router.get("/links")
async def get_all_links():
    return cables.list_fiber_links()

@router.get("/routing/{device_id}")
async def get_routing_table(device_id: str):
    from app.simulation import routing
    return routing.get_routing_table(device_id)

@router.get("/topology/core")
async def get_core_topology():
    # (bereits vorhanden)
    ...

# ✅ NEU
@router.get("/topology/redundancy/{device_id}")
async def get_redundancy(device_id: str):
    devices_list = list(devices.devices.values())
    links_list = cables.list_fiber_links()
    return redundancy.simulate_outage(devices_list, links_list, device_id)
