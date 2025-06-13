from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

router = APIRouter()

class CLIMacro(BaseModel):
    id: str = None
    name: str
    commands: List[str]
    created_at: str = None

cli_macros = []

@router.post("/macro/create", response_model=CLIMacro)
def create_macro(macro: CLIMacro):
    macro.id = str(uuid.uuid4())
    macro.created_at = datetime.utcnow().isoformat()
    cli_macros.append(macro)
    return macro

@router.get("/macro/list", response_model=List[CLIMacro])
def list_macros():
    return cli_macros
