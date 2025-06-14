# C:\noc_project\UltraNOC\backend\app\schemas\device_metrics_schema.py

from pydantic import BaseModel
from datetime import datetime

class DeviceMetricResponse(BaseModel):
    id: str
    device_id: str
    metric_type: str
    value: float
    timestamp: datetime

    class Config:
        orm_mode = True
