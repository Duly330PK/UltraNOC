from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_users():
    return [{"username": "admin", "role": "admin"}]
# C:\noc_project\UltraNOC\backend\app\routers\users.py

from fastapi import APIRouter, Depends
from typing import List
from app.auth.auth_dependency import get_current_user, require_role
from app.models.user import User
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[dict])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    users = db.query(User).all()
    return [
        {
            "username": user.username,
            "role": user.role
        } for user in users
    ]
