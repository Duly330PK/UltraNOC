from fastapi import APIRouter
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter()

class LicenseCheck(BaseModel):
    key: str

@router.post("/check")
def check_license(req: LicenseCheck):
    valid = req.key == "ULTRA-NOC-2025"
    return {
        "license_key": req.key,
        "valid": valid,
        "issued": "2025-01-01",
        "expires": "2026-01-01" if valid else None
    }
