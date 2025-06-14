# C:\noc_project\UltraNOC\backend\app\routers\device_metrics.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.device_metrics import DeviceMetric
from app.schemas.device_metrics_schema import DeviceMetricResponse
from app.database import get_db

router = APIRouter(prefix="/api/v1/metrics", tags=["Metrics"])

@router.get("/", response_model=List[DeviceMetricResponse])
def get_all_metrics(db: Session = Depends(get_db)):
    return db.query(DeviceMetric).all()
