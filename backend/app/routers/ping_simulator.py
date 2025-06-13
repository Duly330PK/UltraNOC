from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

class PingRequest(BaseModel):
    ip: str

@router.post("/ping")
def ping(req: PingRequest):
    reachable = random.choice([True] * 9 + [False])  # 90% reachable
    return {"ip": req.ip, "reachable": reachable}
