# backend/app/routers/topology.py
from fastapi import APIRouter
from app.simulation import redundancy  # später nutzbar

router = APIRouter()

@router.get("/core")
async def get_core_topology():
    return {
        "devices": [
            {
                "id": "core-1",
                "name": "CoreRouter",
                "type": "core",
                "ip": "10.0.0.1",
                "lat": 51.2,
                "lon": 9.0
            },
            {
                "id": "access-1",
                "name": "AccessSwitch",
                "type": "access",
                "ip": "10.0.1.1",
                "lat": 51.3,
                "lon": 9.1
            }
        ]
    }

@router.get("/redundancy/{device_id}")
async def get_redundancy_paths(device_id: str):
    # Beispielhafte Dummy-Daten
    return {
        "primary": [
            {"id": "core-1", "lat": 51.2, "lon": 9.0},
            {"id": "access-1", "lat": 51.3, "lon": 9.1}
        ],
        "backup": [
            {"id": "core-1", "lat": 51.2, "lon": 9.0},
            {"id": "backup-1", "lat": 51.4, "lon": 9.2},
            {"id": "access-1", "lat": 51.3, "lon": 9.1}
        ]
    }
