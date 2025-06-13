from fastapi import APIRouter
from pydantic import BaseModel
import ipaddress

router = APIRouter()

class IPv6Query(BaseModel):
    address: str

@router.post("/validate")
def validate_ipv6(query: IPv6Query):
    try:
        ip = ipaddress.IPv6Address(query.address)
        return {"address": str(ip), "valid": True}
    except ValueError:
        return {"address": query.address, "valid": False}
