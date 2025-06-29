from pydantic import BaseModel
from datetime import datetime

class ForensicsQuery(BaseModel):
    ip_address: str
    port: int
    timestamp: datetime

class ForensicsResult(BaseModel):
    found: bool
    customer_id: str | None = None
    internal_ip: str | None = None
    segment: str | None = None
    device_id: str | None = None