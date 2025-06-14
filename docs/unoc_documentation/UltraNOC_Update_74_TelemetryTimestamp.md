📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📡 UltraNOC – Update 74: Telemetrie-Zeitstempel (UTC-konform)

## 📁 Betroffene Datei

- `backend/app/routers/device_telemetry.py`

---

## 🎯 Ziel

Einführung von standardisierten Zeitstempeln im UTC-Format für eingehende Telemetriedaten. Damit ist eine spätere Korrelation mit Logs, Alarmen und Zeitzonenanalyse möglich.

---

## ⚙️ Änderungen

### 📝 Alt:
```python
entry.timestamp = datetime.utcnow().isoformat()
✅ Neu:
python
Kopieren
Bearbeiten
from datetime import timezone
entry.timestamp = datetime.now(timezone.utc).isoformat()
🧪 Beispiel
POST /push

json
Kopieren
Bearbeiten
{
  "device": "switch-7",
  "cpu_percent": 48.5,
  "mem_percent": 62.1,
  "temperature_c": 38.0
}
Antwort (gekürzt):

json
Kopieren
Bearbeiten
{
  "device": "switch-7",
  "timestamp": "2025-06-14T08:21:44.000Z",
  ...
}
✅ Ergebnisse
Funktion	Status
UTC-Zeit via timezone	✅
ISO-Format für Ausgabe	✅
Kompatibel mit Backend	✅

© 2025 UltraNOC – Telemetriedatenstandardisierung