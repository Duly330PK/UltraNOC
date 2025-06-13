from pydantic import BaseModel
from typing import List
from fastapi import APIRouter
import uuid

router = APIRouter()

fiber_catalog = []

class Fiber(BaseModel):
    id: str
    type: str
    core_count: int
    max_db_loss: float
    application: str

@router.post("/fiber", response_model=Fiber)
def add_fiber(fiber: Fiber):
    fiber.id = str(uuid.uuid4())
    fiber_catalog.append(fiber)
    return fiber

@router.get("/fiber", response_model=List[Fiber])
def get_fibers():
    return fiber_catalog
