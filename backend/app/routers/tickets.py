from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_tickets():
    return [{"ticket_id": "t1", "status": "open"}]
