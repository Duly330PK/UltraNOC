from sqlalchemy import Column, String, Integer, DateTime, BigInteger
from app.database import Base
from datetime import datetime, timezone

class CGNATLog(Base):
    __tablename__ = 'cgnat_session_map'
    session_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="Eindeutige ID der NAT-Session")
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True, comment="Startzeitpunkt der Session (UTC)")
    duration = Column(Integer, default=300, comment="Dauer der Session in Sekunden")
    customer_id = Column(String(100), index=True, comment="Interne Kundenkennung")
    internal_ip = Column(String(45), comment="Private IP des Kunden (z.B. aus 100.64.0.0/10)")
    internal_port = Column(Integer, comment="Privater Port des Kunden")
    external_ip = Column(String(45), index=True, comment="Öffentliche IP des CGNAT-Gateways")
    external_port = Column(Integer, index=True, comment="Gemappter öffentlicher Port")
    protocol = Column(String(4), comment="Protokoll (TCP/UDP)")
    segment = Column(String(20), nullable=True, comment="Optionales internes Routing-Segment oder Tunnel-ID")