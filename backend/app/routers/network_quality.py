from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from random import uniform
import uuid
from datetime import datetime

router = APIRouter()

measurements = []

class QualityMetric(BaseModel):
    id: str
    link_id: str
    delay_ms: float
    jitter_ms: float
    packet_loss_percent: float
    timestamp: str

@router.post("/measure", response_model=QualityMetric)
def simulate_quality(link_id: str):
    metric = QualityMetric(
        id=str(uuid.uuid4()),
        link_id=link_id,
        delay_ms=round(uniform(1, 30), 2),
        jitter_ms=round(uniform(0.1, 10), 2),
        packet_loss_percent=round(uniform(0, 2), 2),
        timestamp=datetime.utcnow().isoformat()
    )
    measurements.append(metric)
    return metric

@router.get("/measurements", response_model=List[QualityMetric])
def list_measurements():
    return measurements
