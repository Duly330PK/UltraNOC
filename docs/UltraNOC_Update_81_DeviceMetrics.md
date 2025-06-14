📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📊 UltraNOC – Update 81: Device Metrics (UTC-Zeitmodell)

## 📁 Datei

- `backend/app/models/device_metrics.py`

---

## 📐 Tabellenmodell `device_metrics`

| Feld         | Typ      | Beschreibung                        |
|--------------|----------|-------------------------------------|
| id           | UUID     | Primärschlüssel                     |
| device_id    | String   | Referenz auf das Gerät              |
| metric_type  | String   | z. B. `cpu`, `rx`, `tx`, `mem`     |
| value        | Float    | Gemessener Wert                     |
| timestamp    | DateTime | UTC-Zeitstempel (automatisch gesetzt) |

---

## 🧠 Zeitumstellung

```python
timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
Kein datetime.utcnow() mehr → Pydantic- & DB-kompatibel

UTC-Zeitbasis → ideal für Multi-Zonen-NOCs & forensische Analysen

🧪 Beispiel-Datensatz
json
Kopieren
Bearbeiten
{
  "device_id": "core-sw1",
  "metric_type": "cpu",
  "value": 18.3,
  "timestamp": "2025-06-13T21:05:14.928Z"
}
🔒 Weitere Hinweise
Wird über device_metrics.py (Router) abgefragt

Getestet in Verbindung mit test_metrics.py (Update 58+)

© 2025 UltraNOC – Device-Metriken mit auditfähiger Zeitbasis