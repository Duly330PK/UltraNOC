from fastapi import APIRouter

router = APIRouter()

@router.post("/exec")
def cli_exec(cmd: str):
    return {"result": f"Simulated exec: {cmd}"}
