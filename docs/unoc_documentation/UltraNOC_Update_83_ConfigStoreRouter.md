📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🧩 UltraNOC – Update 83: config_store.py (API-Router)

## 📂 Pfad

C:\noc_project\UltraNOC\backend\app\routers\config_store.py

yaml
Kopieren
Bearbeiten

---

## 📄 Zweck

Dieser Router verwaltet Gerätekonfigurationen in einer lokalen JSON-Datei (`data/config_store.json`).

---

## 🔧 Funktionen

### POST `/api/v1/config/store`

Speichert eine neue Konfiguration oder überschreibt eine bestehende.

#### Payload:
```json
{
  "device_id": "access-sw1",
  "config_data": "interface Gi0/0\n description Uplink"
}
GET /api/v1/config/load/{device_id}
Lädt die Konfiguration eines bestimmten Geräts.

🧱 Datenmodell (Pydantic)
python
Kopieren
Bearbeiten
class ConfigEntry(BaseModel):
    device_id: str
    config_data: str
💡 Hinweise
Datei wird automatisch angelegt, wenn sie nicht existiert.

Konfigurationen werden als Schlüssel-Wert-Paare (device_id → config_data) gespeichert.

Erweiterbar für Backup, Versionierung oder Geräteklassen.

© 2025 UltraNOC – Modul für konfigurierbare Gerätesimulation