from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

class FirmwareInfo(BaseModel):
    device_id: str
    version: str

@router.post("/upload")
def upload_firmware(info: FirmwareInfo):
    return {
        "status": "uploaded",
        "device_id": info.device_id,
        "version": info.version,
        "timestamp": datetime.utcnow().isoformat()
    }
