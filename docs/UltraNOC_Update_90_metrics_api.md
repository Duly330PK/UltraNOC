📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📊 UltraNOC – Gerätemetriken API

## 📌 Ziel
Einführung eines robusten API-Moduls zur Darstellung und Abfrage von Gerätemetriken (CPU, RAM, RX/TX, etc.). Persistenz über PostgreSQL, abrufbar per GET-Endpoint.

---

## 📁 Komponenten

| Datei | Zweck |
|-------|-------|
| `models/device_metrics.py` | Datenmodell mit UUID, Typ, Wert, Zeitstempel |
| `schemas/device_metrics_schema.py` | Pydantic-Schema zur Rückgabe |
| `routers/device_metrics.py` | API-Router `/api/v1/metrics/` |
| `tests/test_metrics.py` | Test-Client für Abrufverhalten |
| `scripts/init_metrics.sql` | Seed-Daten für Testumgebung |

---

## 🧱 Datenmodell

```python
class DeviceMetric(Base):
    __tablename__ = "device_metrics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String, nullable=False)
    metric_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
📤 GET /api/v1/metrics/
Beispielantwort:
json
Kopieren
Bearbeiten
[
  {
    "id": "b1a6...",
    "device_id": "sw-core-01",
    "metric_type": "cpu",
    "value": 22.5,
    "timestamp": "2025-06-13T14:55:01.823Z"
  }
]
FastAPI-Router:
python
Kopieren
Bearbeiten
@router.get("/", response_model=List[DeviceMetricResponse])
def get_all_metrics(db: Session = Depends(get_db)):
    return db.query(DeviceMetric).all()
🧪 Testfall
python
Kopieren
Bearbeiten
def test_get_all_metrics():
    response = client.get("/api/v1/metrics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
🧬 Schema: device_metrics_schema.py
python
Kopieren
Bearbeiten
class DeviceMetricResponse(BaseModel):
    id: str
    device_id: str
    metric_type: str
    value: float
    timestamp: datetime

    class Config:
        from_attributes = True  # (vormals: orm_mode = True)
🔗 Seed-Daten
sql
Kopieren
Bearbeiten
INSERT INTO device_metrics (device_id, metric_type, value, timestamp)
VALUES ('sw-core-01', 'cpu', 12.5, NOW());
✅ Kompatibel mit OAuth2, Uvicorn, PostgreSQL und Swagger UI.

© 2025 UltraNOC – Gerätemetriken API Dokumentation (Stand: Update 59–63)