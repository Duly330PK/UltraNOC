📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 💾 UltraNOC – Update 65: Config Store API (Gerätekonfiguration)

## 📁 Pfad
C:\noc_project\UltraNOC\docs\UltraNOC_Update_65_ConfigStore_API.md

---

## 🧩 Zielsetzung
Einführung eines persistierenden Speichers für Gerätekonfigurationen.  
Funktionen:
- Speichern beliebiger CLI-/Template-Konfigurationen pro Gerät
- Abruf über eindeutige `device_id`
- Nutzung als Backend für UI-/CLI-Konfigurationsmodule

---

## 📌 Beteiligte Dateien

| Datei                                                                 | Änderungstyp | Zweck                                         |
|-----------------------------------------------------------------------|--------------|-----------------------------------------------|
| backend\app\routers\config_store.py                                   | ✅ Neu       | API-Endpunkte POST /store & GET /load/{id}    |
| data\config_store.json                                                | ✅ Neu       | Beispielhafte Gerätekonfiguration (JSON)      |
| backend\app\main.py                                                   | 🔁 Geändert  | Einbindung des neuen Routers                  |

---

## 🔧 Endpunkte

### `POST /api/v1/config/store`
Speichert Konfiguration zu einer `device_id`

```json
{
  "device_id": "router-1",
  "config_data": "interface Gi0/0\n ip address 192.168.1.1 255.255.255.0"
}
Response:
json
Kopieren
Bearbeiten
{
  "status": "saved",
  "device_id": "router-1"
}
GET /api/v1/config/load/{device_id}
Lädt Konfiguration für das angegebene Gerät

Beispiel:
http
Kopieren
Bearbeiten
GET /api/v1/config/load/router-1
Response:
json
Kopieren
Bearbeiten
{
  "device_id": "router-1",
  "config_data": "interface Gi0/0\n ip address 192.168.1.1 255.255.255.0"
}
🛠️ Technik
Speicherung als JSON-Datei unter /data/config_store.json

Zugriff via Dictionary ({ device_id: config_data })

Validierung via Pydantic BaseModel

Kein Datenbankeintrag – bewusst flach für einfache Tests & UI-Speicherung

🚀 Vorteile
Aspekt	Bewertung
Einfachheit	✅ Hoch
Persistenz	✅ JSON
Integration	✅ RESTful API-konform
Erweiterbar	✅ Für ACL, Tags, Metadata

⏭️ Nächster Schritt
UI/CLI-Integration des Config Store (z. B. über Texteditor oder Upload-Modul)