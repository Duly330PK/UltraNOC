from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserResponse
from app.auth.auth_bearer import require_role

router = APIRouter()

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_role("admin"))])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users