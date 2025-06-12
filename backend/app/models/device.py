from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Device(Base):
    __tablename__ = "devices"
    id = Column(String, primary_key=True)
    hostname = Column(String)
    ip_address = Column(String)
    device_type = Column(String)
    os = Column(String)
    location = Column(String)
    status = Column(String)
