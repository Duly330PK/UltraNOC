from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

class PlaybackRequest(BaseModel):
    session_id: str

@router.get("/playback/{session_id}")
def playback(session_id: str):
    # Mocked response
    return {
        "session_id": session_id,
        "commands": [
            {"timestamp": "2025-06-13T10:00:00", "command": "show ip interface brief"},
            {"timestamp": "2025-06-13T10:00:05", "command": "show version"},
        ],
    }
