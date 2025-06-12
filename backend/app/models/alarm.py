from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()

class Alarm(Base):
    __tablename__ = "alarms"
    id = Column(String, primary_key=True)
    device_id = Column(String)
    type = Column(String)
    severity = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
