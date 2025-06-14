# Pfad: backend/app/routers/path_metrics.py
from fastapi import APIRouter
from typing import List
from datetime import datetime
import random

router = APIRouter()

@router.get("/path/metrics/{source_id}/{target_id}")
async def get_path_metrics(source_id: str, target_id: str):
    # Beispielhafte simulierte Pfaddaten
    simulated_path = [
        {"from": "core1", "to": "bng1"},
        {"from": "bng1", "to": "olt1"},
        {"from": "olt1", "to": "ont1"},
        {"from": "ont1", "to": "cpe1"},
    ]

    # Simuliere Metriken pro Hop
    metrics = []
    for hop in simulated_path:
        metrics.append({
            "from": hop["from"],
            "to": hop["to"],
            "delay_ms": round(random.uniform(1.0, 10.0), 2),
            "loss_percent": round(random.uniform(0.0, 2.0), 2),
            "jitter_ms": round(random.uniform(0.1, 5.0), 2),
            "timestamp": datetime.utcnow().isoformat()
        })

    return {"path": metrics}
