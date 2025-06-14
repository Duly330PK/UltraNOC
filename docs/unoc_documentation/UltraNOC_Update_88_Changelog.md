📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📋 UltraNOC – Changelog Update 60–87

## 🔄 Änderungen im Backend

### ✅ Update 60 – Config Store
- `routers/config_store.py`: Konfigurationsspeicher per JSON
- Neue Datei: `data/config_store.json`
- Endpunkte: `/api/v1/config/store`, `/load/{device_id}`

### ✅ Update 61 – Auth-Login aktiv
- `auth_router.py`: Login via `/api/v1/auth/login`
- Token-Erzeugung über `token_handler.py`
- Nutzerprüfung gegen `models/user.py`

### ✅ Update 62 – Auth-Modelle & TokenHandler
- Pydantic-Schema `auth_schemas.py` ergänzt
- `token_handler.py` modernisiert (.env, UTC-Zeit)

### ✅ Update 63 – UTC-Umstellung
- `device_metrics.py`: DB-Zeitstempel → `datetime.now(timezone.utc)`
- `auth.py`, `device_telemetry.py`: Kompatibel mit neuer Zeitzonenlogik

### ✅ Update 64 – Tokenbasierter Zugriff
- Rolle „admin“ schützt `/api/v1/users/`
- `auth_dependency.py` implementiert
- `users.py` neu erstellt

## 🧪 Tests

- `test_auth.py`: Tokenprüfung & Loginverifikation
- `test_metrics.py`: Zugriff auf Device Metrics

## ⚠️ .env Änderungen

- `DATABASE_URL` als Umgebungsvariable erforderlich
- `SECRET_KEY` aus .env statt Hardcode

## 🔧 Scripts / Seeds

- `init_users.sql`: Admin-Seednutzer
- `init_metrics.sql`: Beispielmetriken
- `create_metrics_table.py`: Tabellenstruktur erzeugen

---

## 🔍 Summary

| Komponente        | Status     | Bemerkung                           |
|-------------------|------------|-------------------------------------|
| Login API         | ✅ aktiv    | via POST `/auth/login`             |
| Token JWT         | ✅ aktiv    | mit Ablaufzeit & Secret Key        |
| Rollenprüfung     | ✅ aktiv    | Abfrage `require_role("admin")`    |
| UTC-Kompatibilität| ✅ vollständig | alle Zeitwerte mit `timezone.utc` |
| Konfigurations-API| ✅ aktiv    | `/config/store` + JSON-Speicher    |
| Tests vorhanden   | ✅          | Login + Metrics getestet           |

---

© 2025 UltraNOC – Modularer NOC-Simulator (Changelog Stand: Update 87)