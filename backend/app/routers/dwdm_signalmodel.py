"""
Update 56 – DWDM Signalpfad-Modul
Ermöglicht die Modellierung von DWDM-Komponenten und -Verbindungen im NOC.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

signal_paths = []

class DWDMComponent(BaseModel):
    id: str
    type: str  # z.B. "Mux", "Demux", "EDFA", "Fiber"
    location: str

class SignalPath(BaseModel):
    id: str = None
    components: List[DWDMComponent]
    wavelength_nm: float
    power_dbm: float
    timestamp: str = None

@router.post("/signalpath", response_model=SignalPath)
def create_signal_path(path: SignalPath):
    path.id = str(uuid.uuid4())
    path.timestamp = datetime.utcnow().isoformat()
    signal_paths.append(path)
    return path

@router.get("/signalpaths", response_model=List[SignalPath])
def list_signal_paths():
    return signal_paths
