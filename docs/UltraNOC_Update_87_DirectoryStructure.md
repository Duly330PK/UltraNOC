📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📁 UltraNOC – Verzeichnisstruktur (Stand: Update 87)

## 🧭 Übersicht

```plaintext
UltraNOC/
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   │   ├── token_handler.py
│   │   │   ├── auth_dependency.py
│   │   ├── core/
│   │   │   └── auth.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── device_metrics.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── auth_router.py
│   │   │   ├── config_store.py
│   │   │   ├── device_metrics.py
│   │   │   ├── device_telemetry.py
│   │   │   ├── users.py
│   │   ├── schemas/
│   │   │   ├── auth_schemas.py
│   │   │   ├── device_metrics_schema.py
│   ├── database.py
│   ├── main.py
│   ├── .env
│   ├── requirements.txt
├── data/
│   └── config_store.json
├── docs/
│   └── *.md (Dokumentation)
├── scripts/
│   ├── create_metrics_table.py
│   ├── init_metrics.sql
│   ├── init_users.sql
├── tests/
│   ├── test_auth.py
│   ├── test_metrics.py
📌 Hinweise
Alle .py-Dateien folgen PEP8

Daten und Konfiguration getrennt (data/, .env)

Seed-Skripte und Migrationshilfen in scripts/

Testfälle vollständig über tests/ abgelegt

.env mit DB-Verbindungsdaten (DATABASE_URL, SECRET_KEY)

✅ Gültigkeit
Diese Struktur bildet den konsolidierten Projektstand nach Updates 60–87 ab und ist Grundlage für CI/CD, Dockerisierung und Deployment.

© 2025 UltraNOC – Projektstruktur & Modularisierung