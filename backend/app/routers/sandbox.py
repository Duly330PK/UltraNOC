# backend/app/routers/sandbox.py

import json
import aiofiles
from fastapi import APIRouter, Request, HTTPException, Depends
from app.auth.auth_bearer import require_role

router = APIRouter(dependencies=[Depends(require_role("admin"))])

SANDBOX_TOPOLOGY_PATH = "app/data/sandbox_topology.json"

@router.get("/load")
async def load_sandbox_topology():
    """Lädt die aktuelle Sandbox-Topologie."""
    try:
        async with aiofiles.open(SANDBOX_TOPOLOGY_PATH, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    except FileNotFoundError:
        # Erstellt eine leere Datei, wenn sie nicht existiert
        async with aiofiles.open(SANDBOX_TOPOLOGY_PATH, "w", encoding="utf-8") as f:
            await f.write(json.dumps({"type": "FeatureCollection", "features": []}))
        return {"type": "FeatureCollection", "features": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load sandbox topology: {e}")

@router.post("/save")
async def save_sandbox_topology(request: Request):
    """Speichert die übermittelte Topologie in der Sandbox-Datei."""
    try:
        topology_data = await request.json()
        async with aiofiles.open(SANDBOX_TOPOLOGY_PATH, "w", encoding="utf-8") as f:
            await f.write(json.dumps(topology_data, indent=4))
        
        # Sim-Engine neu laden, um die Änderungen zu übernehmen
        sim_engine = request.app.state.sim_engine
        sim_engine.reload_topology(SANDBOX_TOPOLOGY_PATH)

        return {"message": "Sandbox topology saved successfully."}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save sandbox topology: {e}")