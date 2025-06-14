📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📊 UltraNOC – Update 66: Device Metrics API

## 📁 Pfad
C:\noc_project\UltraNOC\docs\UltraNOC_Update_66_Device_Metrics_API.md

---

## 🧩 Ziel
Einführung einer persistierten Gerätemetrik-API mit:

- GET-Endpunkt zum Abruf
- Datenbank-Modell für historische Metriken
- UTC-konformer Zeitstempel
- Testabdeckung

---

## 📌 Beteiligte Dateien

| Datei                                                       | Änderungstyp | Funktion                          |
|-------------------------------------------------------------|--------------|-----------------------------------|
| backend\app\models\device_metrics.py                        | 🆕 Modell    | SQLAlchemy-Modell + UTC-Zeit     |
| backend\app\schemas\device_metrics_schema.py                | 🆕 Schema    | Pydantic-Modell (orm_mode)        |
| backend\app\routers\device_metrics.py                       | 🆕 API       | GET /api/v1/metrics/              |
| backend\tests\test_metrics.py                               | 🆕 Test      | API-Test + Felder                 |
| scripts\init_metrics.sql                                    | 🆕 Seed      | Initiale Gerätedaten              |
| scripts\create_metrics_table.py                             | 🆕 Utility   | Tabelle in DB erzeugen           |

---

## 🗄️ Datenbankmodell

```python
class DeviceMetric(Base):
    __tablename__ = "device_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String, nullable=False)
    metric_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
🧾 GET /api/v1/metrics/
Beispiel-Antwort
json
Kopieren
Bearbeiten
[
  {
    "id": "b876f402-4cb3-44ee-a1f2-449e66112e03",
    "device_id": "router-1",
    "metric_type": "cpu",
    "value": 55.3,
    "timestamp": "2025-06-13T18:25:43.511Z"
  }
]
Schema: DeviceMetricResponse
→ orm_mode aktiviert für SQLAlchemy-Kompatibilität

🧪 Tests
test_metrics.py prüft:

Status 200

Rückgabetyp: Liste

Inhalte (z. B. "device_id" in [0])

📂 DB Seed: init_metrics.sql
sql
Kopieren
Bearbeiten
INSERT INTO device_metrics (id, device_id, metric_type, value, timestamp)
VALUES (
  gen_random_uuid(),
  'router-1',
  'cpu',
  55.3,
  CURRENT_TIMESTAMP
);
⚙️ Ergänzende Tools
create_metrics_table.py: Erstellt die Tabelle in dev-DB
.env: Muss korrekt geladen sein (DATABASE_URL)

✅ Vorteile
Feature	Status
DB-Modell	✅
API-Router	✅
UTC-Zeitstempel	✅
Testabdeckung	✅
Seedbarkeit	✅

⏭️ Ausblick
POST zur Einspielung neuer Metriken

Filterung nach device_id, Zeitfenster

Integration in UI (Metrik-Charts)

