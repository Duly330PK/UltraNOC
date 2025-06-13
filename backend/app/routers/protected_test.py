from fastapi import APIRouter, Depends
from app.auth.token_handler import verify_token

router = APIRouter()

@router.get("/api/v1/protected")
def read_protected_data(current_user: str = Depends(verify_token)):
    return {
        "message": f"Willkommen im geschützten Bereich, {current_user}!"
    }
