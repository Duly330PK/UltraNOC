📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📊 UltraNOC – Update 69: Datenmodell `DeviceMetric`

## 📁 Pfad
C:\noc_project\UltraNOC\backend\app\models\device_metrics.py  
C:\noc_project\UltraNOC\docs\UltraNOC_Update_69_Datenmodell_DeviceMetric.md

---

## 🎯 Ziel

Einführung eines persistenten SQLAlchemy-Datenmodells zur Speicherung zeitbasierter Gerätemetriken wie CPU-, Speicher- oder Netzwerk-Auslastung.

---

## 📐 Struktur

### SQLAlchemy-Modell: `DeviceMetric`

```python
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
🔑 Felder im Detail
Feld	Typ	Beschreibung
id	UUID (PK)	Eindeutige ID (automatisch generiert)
device_id	String	ID des Geräts, z. B. core-sw-01
metric_type	String	Typ der Metrik: cpu, rx, temperature
value	Float	Messwert in numerischer Form
timestamp	DateTime (UTC)	Zeitstempel des Messzeitpunkts

📦 Integration
Wird über device_metrics.py angesprochen

Persistiert über init_metrics.sql

Daten abrufbar über API-Endpunkt /api/v1/metrics/

📌 Hinweise
UTC-Zeit wird über datetime.now(timezone.utc) korrekt gehandhabt

Kombinierbar mit Analysefunktionen, Visualisierung, Alarming

🔄 Nächste Schritte
Testabdeckung mit test_metrics.py

Aggregation & Visualisierung im Frontend

© 2025 UltraNOC – Metrikenmodellierung für NOC-Plattformen