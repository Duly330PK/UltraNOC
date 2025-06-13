from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json
import os

router = APIRouter()

# Dynamisch absoluter Pfad zur Szenario-Ordner
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../scenarios"))

class Scenario(BaseModel):
    name: str
    data: dict

@router.get("/scenarios", response_model=List[str])
def list_scenarios():
    return [f for f in os.listdir(BASE_PATH) if f.endswith(".json")]

@router.get("/scenarios/{name}", response_model=Scenario)
def get_scenario(name: str):
    filepath = os.path.join(BASE_PATH, name)
    with open(filepath, "r") as f:
        data = json.load(f)
    return Scenario(name=name, data=data)
