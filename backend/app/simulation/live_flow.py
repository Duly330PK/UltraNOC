from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

flows = []

class TrafficFlow(BaseModel):
    id: str
    src_device: str
    dst_device: str
    bandwidth_mbps: float
    duration_s: int
    timestamp: str

class FlowRequest(BaseModel):
    src_device: str
    dst_device: str
    bandwidth_mbps: float
    duration_s: int

@router.post("/flow", response_model=TrafficFlow)
def add_flow(req: FlowRequest):
    flow = TrafficFlow(
        id=str(uuid.uuid4()),
        src_device=req.src_device,
        dst_device=req.dst_device,
        bandwidth_mbps=req.bandwidth_mbps,
        duration_s=req.duration_s,
        timestamp=datetime.utcnow().isoformat()
    )
    flows.append(flow)
    return flow

@router.get("/flows", response_model=List[TrafficFlow])
def get_flows():
    return flows