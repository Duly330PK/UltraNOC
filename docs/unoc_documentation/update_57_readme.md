**Update 57 - Dokumentation: Getting Started (README)**

---

# UltraNOC - Getting Started

## 🚀 Ziel

Dieses Projekt simuliert ein produktionsnahes Network Operations Center (NOC) inklusive:

- Realistischem Netzwerk- und Gerätemodell
- CLI-Interaktion (Cisco, Nokia, Bash)
- NAT- und Traffic-Simulation
- Rollen- und Benutzerverwaltung
- Topologie-Analyse und Visualisierung
- Vollständiger API-Backbone für Frontend und Tools

## ⚡ Schnellstart

### 1. Backend vorbereiten (Python/FastAPI)

```bash
cd UltraNOC/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. PostgreSQL vorbereiten

```sql
CREATE USER root WITH PASSWORD 'root';
ALTER USER root WITH SUPERUSER;
CREATE DATABASE ultranoc;
\c ultranoc
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

### 3. Datenbank initialisieren

```bash
psql -U root -d ultranoc -f backend/init.sql
```

### 4. Backend starten

```bash
uvicorn app.main:app --reload
```

### 5. Frontend starten (React/Vite)

```bash
cd UltraNOC/frontend
npm install
npm run dev
```

Frontend erreichbar unter: `http://localhost:5173/`

API erreichbar unter: `http://localhost:8000/docs`

## 🌐 API-Dokumentation

Die OpenAPI-Spezifikation ist automatisch generiert unter `/docs` erreichbar.

- GET /api/v1/devices
- POST /api/v1/cli/execute
- u.v.m.

## ⚖️ Tests

```bash
cd UltraNOC/backend
test\run_all_tests.ps1
```

## ✏️ Autoren

- Projektleitung: Matthias B.
- Architektur: GPT-4 (UltraNOC-Assist)

## 📃 Lizenz

MIT License

