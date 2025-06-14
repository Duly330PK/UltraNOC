📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🗂 UltraNOC – Update 70: Config Store API

## 📁 Pfad
C:\noc_project\UltraNOC\backend\app\routers\config_store.py  
C:\noc_project\UltraNOC\data\config_store.json  
C:\noc_project\UltraNOC\docs\UltraNOC_Update_70_ConfigStore_API.md

---

## 🎯 Ziel

Ermöglicht das Speichern und Abrufen von Gerätekonfigurationen als JSON-Struktur – unabhängig von einer relationalen Datenbank.

---

## 📄 Endpunkte

| Methode | Pfad                            | Beschreibung                          |
|--------|----------------------------------|---------------------------------------|
| POST   | `/api/v1/config/store`          | Konfiguration für Gerät speichern     |
| GET    | `/api/v1/config/load/{device_id}` | Konfiguration eines Geräts abrufen    |

---

## 📦 Datenmodell (Pydantic)

```python
from pydantic import BaseModel

class ConfigEntry(BaseModel):
    device_id: str
    config_data: str
🗃 Beispiel: JSON-Datei config_store.json
json
Kopieren
Bearbeiten
{
  "core-router-1": "interface GigabitEthernet0/0\n description Uplink to ISP\n ip address 10.0.0.1 255.255.255.0",
  "core-router-2": "interface GigabitEthernet0/1\n description Backup Uplink\n ip address 10.0.1.1 255.255.255.0"
}
🔐 Sicherheit
Keine Authentifizierung eingebaut (kann per Bearer-Token geschützt werden)

JSON-Datei liegt unter C:\noc_project\UltraNOC\data\config_store.json

Schreib-/Leseoperationen werden atomar ausgeführt (overwrite-safe)

📈 Anwendungsszenarien
Speicherung von CLI-Konfigurationen

Versionierbare Templates (über Erweiterung)

Grundlage für UI-basierte Konfigurationseditoren

🔄 To-Dos
Validierung der config_data-Syntax

Optionale Konfig-Historie

Rechteverwaltung (admin-only)

© 2025 UltraNOC – Persistente Gerätekonfigurationen