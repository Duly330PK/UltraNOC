# C:\noc_project\UltraNOC\backend\app\models\device_metrics.py

from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class DeviceMetric(Base):
    __tablename__ = "device_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String, nullable=False)
    metric_type = Column(String, nullable=False)  # z. B. cpu, mem, rx, tx
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
