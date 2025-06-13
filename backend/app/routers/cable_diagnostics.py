from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

diagnostics_data = []

class CableDiagnostic(BaseModel):
    id: str = None
    cable_id: str
    attenuation_db: float
    length_m: float
    result: str = None
    timestamp: str = None

class CableTest(BaseModel):
    cable_id: str

@router.post("/run", response_model=CableDiagnostic)
def run_diagnostic(entry: CableDiagnostic):
    entry.id = str(uuid.uuid4())
    entry.timestamp = datetime.utcnow().isoformat()
    entry.result = "PASS" if entry.attenuation_db < 5.0 else "FAIL"
    diagnostics_data.append(entry)
    return entry

@router.get("/results", response_model=List[CableDiagnostic])
def get_results():
    return diagnostics_data

@router.post("/diagnose")
def diagnose_cable(req: CableTest):
    return {
        "id": str(uuid.uuid4()),
        "cable_id": req.cable_id,
        "length_m": 137,
        "status": "ok",
        "loss_db": 0.8,
        "timestamp": datetime.utcnow().isoformat()
    }
