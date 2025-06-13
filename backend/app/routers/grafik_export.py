from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter()

EXPORT_PATH = "export"

@router.post("/screenshot")
def export_map_image():
    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)
    # Dummy-Erstellung, später durch UI-Png ersetzt
    path = os.path.join(EXPORT_PATH, f"map_{datetime.utcnow().timestamp()}.svg")
    with open(path, "w") as f:
        f.write("<svg><text x='10' y='20'>Mock TopoMap Export</text></svg>")
    return {"status": "created", "path": path}
