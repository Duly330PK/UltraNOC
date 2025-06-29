from fastapi import APIRouter, Depends, Request
from app.auth.auth_bearer import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/")
def get_topology(request: Request, current_user: User = Depends(get_current_user)):
    sim_engine = request.app.state.sim_engine
    return sim_engine.get_full_topology()