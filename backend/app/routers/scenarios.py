import json
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
from app.auth.auth_bearer import require_role

router = APIRouter(dependencies=[Depends(require_role("admin"))])

def _load_scenario(name: str):
    try:
        # Construct a safe path to the scenarios directory
        # This prevents directory traversal attacks
        base_path = "app/data/scenarios"
        safe_name = name.replace("..", "").replace("/", "").replace("\\", "")
        file_path = f"{base_path}/{safe_name}.json"

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Szenario '{name}' nicht gefunden.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Szenario-Datei konnte nicht gelesen werden: {e}")

async def _execute_scenario(sim_engine, steps: list):
    for step in steps:
        await asyncio.sleep(step.get("delay_s", 1))
        action = step.get("action")
        target_id = step.get("target_id")
        payload = step.get("payload")

        if not all([action, target_id, payload]):
            print(f"Skipping invalid step in scenario: {step}")
            continue

        if action == "set_status":
            await sim_engine.update_device_status(target_id, payload.get("status"), "Scenario")
        # Here, more actions for scenarios could be implemented in the future.

@router.post("/load/{scenario_name}", status_code=202)
async def load_scenario(scenario_name: str, request: Request, background_tasks: BackgroundTasks):
    sim_engine = request.app.state.sim_engine
    scenario_data = _load_scenario(scenario_name)
    background_tasks.add_task(_execute_scenario, sim_engine, scenario_data.get("steps", []))
    return {"message": f"Szenario '{scenario_data.get('name', 'Unbenannt')}' wurde gestartet."}