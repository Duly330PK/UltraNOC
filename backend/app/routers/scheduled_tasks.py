from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

router = APIRouter()

scheduled_tasks = []

class ScheduledTask(BaseModel):
    id: str = None
    task: str
    run_at: str

@router.post("/add")
def add_task(task: ScheduledTask):
    task.id = str(uuid.uuid4())
    scheduled_tasks.append(task)
    return task

@router.get("/list", response_model=List[ScheduledTask])
def list_tasks():
    return scheduled_tasks
