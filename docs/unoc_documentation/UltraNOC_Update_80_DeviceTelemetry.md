📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📡 UltraNOC – Update 80: Telemetrie-Datenempfang (device_telemetry.py)

## 📁 Datei

- `backend/app/routers/device_telemetry.py`

---

## 🚀 Funktionalität

| Endpunkt             | Methode | Beschreibung                                |
|----------------------|---------|---------------------------------------------|
| `/push`              | POST    | Fügt neuen Telemetrieeintrag hinzu          |
| `/latest`            | GET     | Gibt die aktuelle Liste aller Einträge zurück|

---

## 📦 Beispiel-Datenmodell

```json
{
  "device": "router-1",
  "cpu_percent": 42.7,
  "mem_percent": 81.2,
  "temperature_c": 65.4
}
⏱️ Zeitstempel (UTC-konform)
python
Kopieren
Bearbeiten
entry.timestamp = datetime.now(timezone.utc).isoformat()
Verwendet Zeitzone „UTC“ explizit → Auditfähig & zukunftssicher

✅ Struktur intern
python
Kopieren
Bearbeiten
telemetry_data = []
Temporärer Speicher → später durch persistente Lösung ersetzbar

Kann leicht durch InfluxDB, Timescale o.ä. substituiert werden

🔐 Sicherheit
Aktuell offen (kein Auth-Schutz) → folgt in Update 67+

Anbindung an Token-/Rollenlogik geplant

🛠 Beispieltest mit curl
bash
Kopieren
Bearbeiten
curl -X POST http://localhost:8000/push \
  -H "Content-Type: application/json" \
  -d '{"device":"sw-core-1","cpu_percent":15,"mem_percent":70,"temperature_c":55}'
© 2025 UltraNOC – Echtzeitdaten & verlässliche UTC-Zeitbasis für Netzwerk-Telemetrie