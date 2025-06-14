
**Body:**

```json
{
  "device_id": "core-router-1",
  "config_data": "interface Gig0/0\n ip address 10.0.0.1 255.255.255.0"
}
Response:

json
Kopieren
Bearbeiten
{
  "status": "saved",
  "device_id": "core-router-1"
}
GET /api/v1/config/load/{device_id}
Lädt die gespeicherte Konfiguration eines bestimmten Geräts.

Beispiel:

GET /api/v1/config/load/core-router-1

Response:

json
Kopieren
Bearbeiten
{
  "device_id": "core-router-1",
  "config_data": "interface Gig0/0\n ip address 10.0.0.1 255.255.255.0"
}
🧾 Datenmodell
python
Kopieren
Bearbeiten
class ConfigEntry(BaseModel):
    device_id: str
    config_data: str
💾 Datei: config_store.json
json
Kopieren
Bearbeiten
{
  "core-router-1": "interface GigabitEthernet0/0\n description Uplink to ISP\n ip address 10.0.0.1 255.255.255.0",
  "core-router-2": "interface GigabitEthernet0/1\n description Backup Uplink\n ip address 10.0.1.1 255.255.255.0"
}
✅ Vorteile
Feature	Status
Persistenz (JSON-Datei)	✅
API-basierte Schnittstelle	✅
Geräteselektiv abrufbar	✅
UI-/CLI-ready	✅

⏭️ Ausblick
Validierung und Versionskontrolle von Konfigurationen

CLI-Import/Export

UI-Integration zur Visualisierung und Bearbeitung

