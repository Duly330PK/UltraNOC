from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

preferences = {}

class Preference(BaseModel):
    username: str
    settings: Dict[str, str]

@router.post("/save")
def save_preferences(pref: Preference):
    preferences[pref.username] = pref.settings
    return {"status": "saved", "user": pref.username}

@router.get("/load/{username}")
def load_preferences(username: str):
    return preferences.get(username, {})
