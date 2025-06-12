from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import datetime

router = APIRouter()

failures = []

class FailoverEvent(BaseModel):
    id: str
    affected_link: str
    timestamp: str
    rerouted: bool
    impacted_devices: List[str]

@router.post("/simulate/link-down", response_model=FailoverEvent)
def simulate_link_failure(link_id: str):
    event = FailoverEvent(
        id=f"fail-{link_id}-{datetime.datetime.now().timestamp()}",
        affected_link=link_id,
        timestamp=datetime.datetime.utcnow().isoformat(),
        rerouted=True,
        impacted_devices=["core1", "sw3"]
    )
    failures.append(event)
    return event

@router.get("/failures", response_model=List[FailoverEvent])
def list_failures():
    return failures
