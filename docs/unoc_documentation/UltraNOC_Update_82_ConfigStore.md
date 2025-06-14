📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🗄️ UltraNOC – Update 82: Config Store (Gerätekonfigurationen)

## 📁 Dateien

- `backend/app/routers/config_store.py`
- `data/config_store.json`

---

## 🎯 Ziel

- Speicherung und Abruf von CLI-Konfigurationen pro Gerät
- Datenhaltung in persistenter JSON-Datei
- API-gesteuerte Verwaltung (GET / POST)

---

## 🧩 API-Endpunkte

| Methode | Pfad                       | Beschreibung                          |
|--------|----------------------------|----------------------------------------|
| POST   | `/api/v1/config/store`     | Konfiguration für Gerät speichern     |
| GET    | `/api/v1/config/load/{id}` | Konfiguration für Gerät abrufen       |

---

## 📦 Beispiel – `config_store.json`

```json
{
  "core-router-1": "interface Gi0/0\n description Uplink\n ip address 10.0.0.1 255.255.255.0",
  "core-router-2": "interface Gi0/1\n description Backup\n ip address 10.0.1.1 255.255.255.0"
}
🔐 Sicherheit
Noch ungeschützt – Erweiterung durch Auth-Decorator empfohlen

Schreib-/Leserechte durch Adminrollen möglich (Update 66+)

🧪 Beispielaufrufe (curl)
bash
Kopieren
Bearbeiten
curl -X POST http://localhost:8000/api/v1/config/store \
  -H "Content-Type: application/json" \
  -d '{"device_id": "access-sw1", "config_data": "hostname access-sw1"}'
© 2025 UltraNOC – Persistente Konfigurationsverwaltung für Netzwerkgeräte