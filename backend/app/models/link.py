from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Link(Base):
    __tablename__ = "links"
    id = Column(String, primary_key=True)
    from_device = Column(String)
    to_device = Column(String)
    status = Column(String)
    fiber_type = Column(String)
