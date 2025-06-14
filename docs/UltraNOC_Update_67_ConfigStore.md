📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🧩 UltraNOC – Update 67: Config Store API

## 📁 Pfad
C:\noc_project\UltraNOC\docs\UltraNOC_Update_67_ConfigStore.md

---

## 🎯 Ziel

Einführung eines persistierbaren Speichers für Gerätekonfigurationen in JSON-Form – zur späteren Analyse, UI-Darstellung oder Wiederherstellung.

---

## 📚 Beteiligte Dateien

| Datei                                             | Zweck                                |
|--------------------------------------------------|--------------------------------------|
| app\routers\config_store.py                      | REST-API zum Speichern/Laden         |
| data\config_store.json                           | Ablageort der Gerätekonfigurationen  |

---

## 🔌 Endpunkte

### POST /api/v1/config/store

Speichert eine Konfiguration.

**Request Body (JSON):**

```json
{
  "device_id": "core-router-1",
  "config_data": "interface g0/0\n ip address ..."
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
Lädt Konfiguration für ein spezifisches Gerät.

Beispiel:

http
Kopieren
Bearbeiten
GET /api/v1/config/load/core-router-1
Response:

json
Kopieren
Bearbeiten
{
  "device_id": "core-router-1",
  "config_data": "interface g0/0\n ip address ..."
}
💾 Datei: config_store.json
Strukturbeispiel:

json
Kopieren
Bearbeiten
{
  "core-router-1": "interface g0/0\n ip address 10.0.0.1 255.255.255.0",
  "core-router-2": "interface g0/1\n ip address 10.0.1.1 255.255.255.0"
}
🔐 Sicherheit & Schutzmaßnahmen
Keine Authentifizierung aktuell aktiv – für Produktionsbetrieb später absichern!

Schreibzugriff per POST – künftig rollenbasiert absichern

JSON-File-basierte Speicherung – ideal für kleine bis mittlere Datenmengen

📈 Erweiterungsideen
Funktion	Status
CLI-Konfigurationen speichern	✅
Wiederherstellung via API	✅
GUI-Anbindung in Planung	🔄
Diff-/Versionierung	⏳

© 2025 UltraNOC – Config Store API