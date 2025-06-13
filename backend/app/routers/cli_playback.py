from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid

router = APIRouter()

# In-Memory CLI-Playback-Store (ersetzbar durch DB später)
playback_store = {}

class CLICommand(BaseModel):
    session_id: str
    command: str
    timestamp: str = None

@router.post("/record", response_model=dict)
def record_command(entry: CLICommand):
    entry.timestamp = datetime.utcnow().isoformat()
    if entry.session_id not in playback_store:
        playback_store[entry.session_id] = []
    playback_store[entry.session_id].append(entry)
    return { "status": "recorded", "session_id": entry.session_id }

@router.get("/playback/{session_id}", response_model=List[CLICommand])
def get_history(session_id: str, command_filter: Optional[str] = Query(None)):
    history = playback_store.get(session_id, [])
    if command_filter:
        return [cmd for cmd in history if command_filter in cmd.command]
    return history

@router.get("/commands/map")
def get_command_summary():
    summary = {}
    for session_id, commands in playback_store.items():
        summary[session_id] = len(commands)
    return summary
