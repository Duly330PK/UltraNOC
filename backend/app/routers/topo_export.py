from fastapi import APIRouter
import os
from datetime import datetime

router = APIRouter()

EXPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "export"))
os.makedirs(EXPORT_DIR, exist_ok=True)

@router.post("/generate")
def generate_svg():
    filename = f"topo_{datetime.utcnow().timestamp():.0f}.svg"
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w") as f:
        f.write("<svg><text x='10' y='20'>Topology Snapshot</text></svg>")
    return {"status": "created", "path": path}
