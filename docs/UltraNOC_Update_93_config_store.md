📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🧾 UltraNOC – Config Store (Gerätekonfigurationen)

## 📌 Ziel
Speichern und Abrufen von Gerätekonfigurationen in persistenter Form. 
Verwendung für UI-Vorschau, CLI-Wiedergabe, Konfigvergleich und Auditing.

---

## 🔧 Architektur

| Komponente | Funktion |
|------------|----------|
| `routers/config_store.py` | API-Router |
| `data/config_store.json` | Konfigspeicher (JSON-Datei) |

---

## 📤 API – Endpunkte

| Methode | Pfad | Beschreibung |
|--------|------|--------------|
| POST | `/api/v1/config/store` | Speichert Konfiguration für Gerät |
| GET | `/api/v1/config/load/{device_id}` | Lädt Konfiguration für ein Gerät |

---

## 🧩 Beispielstruktur – JSON-Format

```json
{
  "core-router-1": "interface G0/0\n description Uplink\n ip address 10.0.0.1 255.255.255.0",
  "core-router-2": "interface G0/1\n description Backup\n ip address 10.0.1.1 255.255.255.0"
}
Formatierung: reiner String

Schlüssel: device_id

Speicherort: C:\noc_project\UltraNOC\data\config_store.json

✅ Datenmodell
python
Kopieren
Bearbeiten
class ConfigEntry(BaseModel):
    device_id: str
    config_data: str
💡 Nutzungsszenarien
GUI-Konfigeditor

Textvergleich / Backup-Analyse

Wiederherstellung historischer Zustände

CLI-Mitschnitt-Management

© 2025 UltraNOC – Config Store API (Update 60)

perl
Kopieren
Bearbeiten
