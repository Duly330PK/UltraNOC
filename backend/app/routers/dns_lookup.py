from fastapi import APIRouter
from pydantic import BaseModel
import socket

router = APIRouter()

class DNSQuery(BaseModel):
    hostname: str

@router.post("/lookup")
def dns_lookup(query: DNSQuery):
    try:
        ip = socket.gethostbyname(query.hostname)
        return {"hostname": query.hostname, "ip": ip}
    except Exception as e:
        return {"error": str(e)}
