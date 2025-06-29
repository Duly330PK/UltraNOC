# backend/app/routers/simulation_actions.py

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
from pydantic import BaseModel
from app.auth.auth_bearer import get_current_user
from app.models.user import User

router = APIRouter()

class TogglePayload(BaseModel):
    enabled: bool

@router.post("/security/toggle", status_code=200)
async def toggle_security_simulation(payload: TogglePayload, request: Request, user: User = Depends(get_current_user)):
    """Schaltet die Generierung von Sicherheits-Events an oder aus."""
    sim_engine = request.app.state.sim_engine
    sim_engine.security_simulation_enabled = payload.enabled
    status = "aktiviert" if payload.enabled else "deaktiviert"
    print(f"Sicherheits-Simulation durch '{user.username}' {status}.")
    return {"message": f"Sicherheits-Event-Generierung wurde {status}."}

@router.post("/security/reset", status_code=202)
async def reset_security_simulation(request: Request, user: User = Depends(get_current_user)):
    """Setzt alle Sicherheits-Events und Incidents zurück."""
    sim_engine = request.app.state.sim_engine
    background_tasks = BackgroundTasks()
    background_tasks.add_task(sim_engine.reset_security_events)
    print(f"Reset der Sicherheits-Events durch '{user.username}' angestoßen.")
    return {"message": "Reset für Sicherheits-Events wurde gestartet."}


@router.post("/devices/{device_id}/action", status_code=202)
async def perform_device_action(
    device_id: str,
    action: dict,
    request: Request,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user)
):
    sim_engine = request.app.state.sim_engine
    action_type = action.get("type")
    payload = action.get("payload", {})
    
    if not sim_engine.get_node_by_id(device_id):
        raise HTTPException(status_code=404, detail=f"Device {device_id} not found.")

    actor = f"User '{user.username}'"

    if action_type == "set_status":
        new_status = payload.get("status")
        if not new_status:
            raise HTTPException(status_code=400, detail="Status not provided")
        background_tasks.add_task(sim_engine.update_device_status, device_id, new_status, actor)
        return {"message": f"Task to set status for {device_id} to {new_status} started."}
        
    elif action_type == "reboot":
        background_tasks.add_task(sim_engine.reboot_device, device_id, actor)
        return {"message": f"Reboot sequence for {device_id} initiated."}
        
    elif action_type == "get_cli_output":
        command = payload.get("command")
        if not command:
            raise HTTPException(status_code=400, detail="Command not provided")
        output = sim_engine.get_cli_output(device_id, command)
        return {"output": output}

    raise HTTPException(status_code=400, detail="Invalid action type")