📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🗂️ UltraNOC – Update 73: Config Store (Gerätekonfigurationen)

## 📁 Betroffene Dateien

- `backend/app/routers/config_store.py`
- `data/config_store.json`
- `main.py` (Router-Einbindung)

---

## 🎯 Ziel

Persistente Speicherung von Gerätekonfigurationen (z. B. CLI-Ausgaben, Interfaces, Templates) im JSON-Format. Ermöglicht später UI-Anbindung, Exporte und Wiederherstellung.

---

## 🔧 Endpunkte

### 📥 POST `/api/v1/config/store`

Speichert Konfiguration für ein bestimmtes Gerät.

**Body:**
```json
{
  "device_id": "router-1",
  "config_data": "interface gi0/0\n description Uplink"
}
Antwort:

json
Kopieren
Bearbeiten
{
  "status": "saved",
  "device_id": "router-1"
}
📤 GET /api/v1/config/load/{device_id}
Lädt Konfiguration für ein Gerät.

Antwort (Beispiel):

json
Kopieren
Bearbeiten
{
  "device_id": "router-1",
  "config_data": "interface gi0/0\n description Uplink"
}
🗄 Datei: data/config_store.json
Initialer Inhalt:

json
Kopieren
Bearbeiten
[
  {
    "device_id": "core-router-1",
    "config_data": "interface gi0/0\n description Uplink to ISP"
  }
]
🔐 Fehlerfälle
Gerät nicht gefunden → 404: Device config not found

Datei fehlt → 404: No config data found

✅ Ergebnisse
Funktion	Status
Konfiguration speichern/laden	✅
Fehlerbehandlung für fehlende Geräte	✅
JSON-Dateibasiert	✅
API testbar per Postman / CLI	✅

© 2025 UltraNOC – Gerätekonfiguration im JSON-Speicher