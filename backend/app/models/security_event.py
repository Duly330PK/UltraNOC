from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Incident(Base):
    __tablename__ = 'incidents'
    id = Column(Integer, primary_key=True, index=True, comment="Eindeutige ID des Sicherheitsvorfalls")
    title = Column(String(255), index=True, comment="Titel des Incidents (z.B. 'Brute-Force-Angriff')")
    description = Column(Text, comment="Vom LLM generierte Zusammenfassung des Vorfalls")
    status = Column(String(50), default="Pending", comment="Status: Pending, In Progress, Resolved, Closed")
    assignee = Column(String(100), nullable=True, comment="Zugewiesener Analyst")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    events = relationship("SecurityEvent", back_populates="incident", cascade="all, delete-orphan")

class SecurityEvent(Base):
    __tablename__ = 'security_events'
    id = Column(Integer, primary_key=True, index=True, comment="Eindeutige ID des Sicherheitsereignisses")
    incident_id = Column(Integer, ForeignKey('incidents.id'), nullable=True, comment="Zugehöriger Incident, falls korreliert")
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    type = Column(String(100), comment="Art des Ereignisses (z.B. 'Failed SSH login')")
    description = Column(Text, comment="Detaillierte Beschreibung des Events")
    source_ip = Column(String(45), nullable=True, comment="Quell-IP des Ereignisses")
    target_node_id = Column(String(100), nullable=True, comment="Zielgerät des Ereignisses")
    details = Column(JSON, nullable=True, comment="Zusätzliche Metadaten als JSON-Objekt")
    incident = relationship("Incident", back_populates="events")