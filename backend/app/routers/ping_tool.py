from fastapi import APIRouter
from pydantic import BaseModel
import subprocess

router = APIRouter()

class PingRequest(BaseModel):
    target: str

@router.post("/ping")
def ping_host(req: PingRequest):
    try:
        output = subprocess.check_output(
            ["ping", "-n", "2", req.target],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=5
        )
        return {
            "target": req.target,
            "status": "reachable",
            "output": output
        }
    except subprocess.CalledProcessError as e:
        return {
            "target": req.target,
            "status": "unreachable",
            "error": e.output
        }
    except Exception as e:
        return {
            "target": req.target,
            "status": "error",
            "error": str(e)
        }
