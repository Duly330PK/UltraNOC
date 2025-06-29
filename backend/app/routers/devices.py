# backend/app/routers/devices.py

from fastapi import APIRouter, Depends, Request
from typing import List, Optional
from pydantic import BaseModel

# Wir definieren hier ein einfaches Schema für die Geräteantwort, 
# um nicht die gesamte komplexe GeoJSON-Struktur zu senden.
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
    skip: int = 0, # Wie viele Einträge sollen übersprungen werden (für Paginierung)
    limit: int = 50, # Wie viele Einträge sollen pro Seite zurückgegeben werden
    search: Optional[str] = None # Optionaler Suchparameter
):
    """
    Liefert eine durchsuchbare und paginierbare Liste aller Geräte.
    """
    sim_engine = request.app.state.sim_engine
    
    # Holen Sie alle Knoten aus der Simulation
    all_nodes = list(sim_engine.node_map.values())
    
    # Filterung basierend auf dem Suchbegriff (falls vorhanden)
    if search:
        search = search.lower()
        filtered_nodes = [
            node for node in all_nodes 
            if search in node['properties'].get('id', '').lower() or \
               search in node['properties'].get('label', '').lower() or \
               search in node['properties'].get('type', '').lower()
        ]
    else:
        filtered_nodes = all_nodes

    total_count = len(filtered_nodes)
    
    # Paginierung anwenden
    paginated_nodes = filtered_nodes[skip : skip + limit]
    
    # Konvertiere die gefilterten und paginierten Knoten in unser Device-Schema
    devices_for_response = []
    for node in paginated_nodes:
        props = node['properties']
        devices_for_response.append(Device(
            id=props.get('id'),
            label=props.get('label'),
            type=props.get('type'),
            status=props.get('status', 'unknown')
        ))
        
    return DeviceResponse(total_count=total_count, devices=devices_for_response)