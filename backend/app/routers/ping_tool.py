from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import uuid
from datetime import datetime

router = APIRouter()

class PingRequest(BaseModel):
    target: str

@router.post("/ping")
def ping_host(req: PingRequest):
    try:
        output = subprocess.check_output(["ping", "-n", "2", req.target], stderr=subprocess.STDOUT, universal_newlines=True, timeout=5)
        return {"status": "reachable", "target": req.target, "output": output}
    except subprocess.CalledProcessError as e:
        return {"status": "unreachable", "target": req.target, "output": e.output}
    except Exception as e:
        return {"status": "error", "message": str(e)}
