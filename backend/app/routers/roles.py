from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()

roles = []

class Role(BaseModel):
    id: str
    name: str
    permissions: List[str]

@router.post("/", response_model=Role)
def create_role(role: Role):
    role.id = str(uuid.uuid4())
    roles.append(role)
    return role

@router.get("/", response_model=List[Role])
def list_roles():
    return roles
