# backend/app/routers/devices.py

from fastapi import APIRouter, Depends, Request
from typing import List, Optional
from pydantic import BaseModel

class Device(BaseModel):
    id: str
    label: str
    type: str
    status: str

class DeviceResponse(BaseModel):
    total_count: int
    devices: List[Device]

router = APIRouter()

@router.get("/", response_model=DeviceResponse)
def get_device_list(
    request: Request,
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None
):
    sim_engine = request.app.state.sim_engine
    all_nodes = list(sim_engine.node_map.values())
    
    # Filter nodes that have the necessary properties to be considered a device
    valid_devices = [
        node for node in all_nodes 
        if 'id' in node.get('properties', {}) and 'label' in node.get('properties', {}) and 'type' in node.get('properties', {})
    ]

    if search:
        search = search.lower()
        filtered_nodes = [
            node for node in valid_devices 
            if search in node['properties']['id'].lower() or \
               search in node['properties']['label'].lower() or \
               search in node['properties']['type'].lower()
        ]
    else:
        filtered_nodes = valid_devices

    total_count = len(filtered_nodes)
    paginated_nodes = filtered_nodes[skip : skip + limit]
    
    devices_for_response = [
        Device(
            id=node['properties']['id'],
            label=node['properties']['label'],
            type=node['properties']['type'],
            status=node['properties'].get('status', 'unknown')
        ) for node in paginated_nodes
    ]
        
    return DeviceResponse(total_count=total_count, devices=devices_for_response)