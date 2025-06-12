from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_audit_logs():
    return [{"user": "admin", "action": "conf t", "timestamp": "2025-06-11T10:00:00Z"}]
