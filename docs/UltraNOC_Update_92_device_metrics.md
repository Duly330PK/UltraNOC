📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📊 UltraNOC – Gerätemetriken (device_metrics)

## 📌 Ziel
Erfassung und Bereitstellung von Gerätemetriken (CPU, RAM, RX/TX etc.) für Auswertung, UI-Darstellung und forensische Analyse.

---

## 🔧 Architektur

| Komponente | Funktion |
|------------|----------|
| `models/device_metrics.py` | SQLAlchemy-Modell |
| `schemas/device_metrics_schema.py` | Pydantic-Responsemodell |
| `routers/device_metrics.py` | API-Router |
| `tests/test_metrics.py` | Integrationstest |
| `scripts/init_metrics.sql` | Seed-Daten für Testumgebung |

---

## 🧩 Datenmodell (device_metrics)

```python
class DeviceMetric(Base):
    id: UUID (primary key)
    device_id: str
    metric_type: str  # cpu / mem / rx / tx
    value: float
    timestamp: datetime (UTC)
Zeitzone: datetime.now(timezone.utc)

📤 API – Endpunkt
Methode	Pfad	Beschreibung
GET	/api/v1/metrics/	Gibt alle gespeicherten Gerätemetriken zurück

🧾 Pydantic-Schema
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
        from_attributes = True  # Pydantic v2
✅ Test – test_metrics.py
Statuscode 200

Rückgabe: Liste mit Feldern

optionaler Inhaltstest auf device_id, metric_type, value, timestamp

🔁 Seed-Daten – init_metrics.sql
Fügt Demo-Daten ein zur sofortigen Abfrage.

📈 Ausbaustufe:

Späterer Filter via Query-Parameter (device_id, Zeitraum)

Exportfunktion (CSV, Grafana-Feed)

Realtime-Erweiterung mit WebSocket

© 2025 UltraNOC – Metrics API (Update 59+)

perl
Kopieren
Bearbeiten
