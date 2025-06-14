📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📊 UltraNOC – Device Metrics API

## 📌 Ziel
Bereitstellung von Gerätemetriken wie CPU, Speichernutzung oder Bandbreite zur Visualisierung im Dashboard.

---

## 📦 Komponenten

| Pfad | Funktion |
|------|----------|
| `models/device_metrics.py` | SQLAlchemy-Modell für Metrics |
| `routers/device_metrics.py` | API-Router für GET-Abfrage |
| `schemas/device_metrics_schema.py` | Pydantic-Response-Modell |
| `tests/test_metrics.py` | API-Test mit FastAPI TestClient |
| `scripts/init_metrics.sql` | Seed-Daten für Testumgebung |

---

## 🧩 Datenmodell (SQLAlchemy)

```python
class DeviceMetric(Base):
    id: UUID
    device_id: str
    metric_type: str  # z. B. cpu, mem, rx, tx
    value: float
    timestamp: datetime
→ Zeitzone: datetime.now(timezone.utc) für Kompatibilität

🧾 Response-Modell (Pydantic)
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
        from_attributes = True
📤 Endpunkt
Methode	Pfad	Beschreibung
GET	/api/v1/metrics/	Liefert alle Gerätemetriken

✅ Testabdeckung
python
Kopieren
Bearbeiten
def test_get_all_metrics():
    response = client.get("/api/v1/metrics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        assert "device_id" in response.json()[0]
🗂 Zusatz
Seed-Datei: scripts/init_metrics.sql
Beispieldaten: CPU/MEM-Auslastung für Router

© 2025 UltraNOC – Device Metrics API (Update 59–61)