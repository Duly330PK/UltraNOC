from fastapi import APIRouter
import uuid
from datetime import datetime

router = APIRouter()

incidents = []

@router.post("/raise")
def raise_incident(source: str, impact: str):
    entry = {
        "id": str(uuid.uuid4()),
        "source": source,
        "impact": impact,
        "timestamp": datetime.utcnow().isoformat()
    }
    incidents.append(entry)
    return entry

@router.get("/summary")
def get_summary():
    return incidents
