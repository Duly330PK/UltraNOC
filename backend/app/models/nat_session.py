from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()

class NATSession(Base):
    __tablename__ = "nat_sessions"
    session_id = Column(String, primary_key=True, index=True)
    src_internal = Column(String)
    src_port = Column(Integer)
    mapped_ip = Column(String)
    mapped_port = Column(Integer)
    dst_ip = Column(String)
    dst_port = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
