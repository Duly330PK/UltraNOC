# 🧠 UltraNOC – Lokale Installation (Windows)

Dies ist die Schritt-für-Schritt-Anleitung zur lokalen Einrichtung und Ausführung des UltraNOC-Projekts in einer Windows-Umgebung mit PowerShell.

---

## ⚙️ Systemvoraussetzungen

Stelle sicher, dass auf deinem System folgendes installiert ist:

- ✅ **Python 3.10+**
- ✅ **Node.js 18+** (inkl. `npm`)
- ✅ **PostgreSQL 14+** (Benutzer: `root`, Passwort: `root`)
- ✅ **Git** (optional für Erweiterungen)
- ✅ **PowerShell (als Admin empfohlen)**

---

## 📁 Projektstruktur

Du hast das Projekt in folgendem Pfad:

```plaintext
C:\noc_project\UltraNOC\
🔧 1. Backend vorbereiten
powershell
Copy
Edit
cd C:\noc_project\UltraNOC\backend

# Virtuelle Umgebung erstellen
python -m venv venv
.\venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
🗃 2. Datenbank initialisieren
PostgreSQL-Datenbank muss lokal laufen (Port 5432)

powershell
Copy
Edit
# Datenbank erzeugen (nur einmal erforderlich)
psql -U root -c "CREATE DATABASE ultranoc;"

# Struktur einspielen
psql -U root -d ultranoc -f init.sql
Falls psql nicht im Pfad: Nutze pgAdmin oder %ProgramFiles%\PostgreSQL\<version>\bin\psql.exe

🚀 3. Backend starten (FastAPI)
powershell
Copy
Edit
cd C:\noc_project\UltraNOC\backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
API läuft dann auf: http://localhost:8000/docs

🌐 4. Frontend installieren & starten
powershell
Copy
Edit
cd C:\noc_project\UltraNOC\frontend
npm install
npm run dev
Frontend erreichbar unter: http://localhost:3000

🔐 5. Standardbenutzer anlegen (optional)
powershell
Copy
Edit
cd C:\noc_project\UltraNOC\scripts
python init_users.py
Erstellt z. B. einen Admin mit:

Benutzer: admin

Passwort: admin123

🧪 6. Testbefehle (im UI oder CLI)
Login im Web (UI)

Öffne CLI-Konsole

Führe aus:

bash
Copy
Edit
show interfaces
conf t
interface g0/0
ip address 10.0.0.1 255.255.255.0
🧠 Weitere Befehle (optional)
Ausfall simulieren:

bash
Copy
Edit
simulate link-down LINKID
NAT-Verfolgung:

bash
Copy
Edit
show ip nat translations
📄 .env Beispiel
Kopiere .env.example → .env und passe bei Bedarf DB-Zugang an.

ini
Copy
Edit
DB_HOST=localhost
DB_PORT=5432
DB_USER=root
DB_PASSWORD=root
DB_NAME=ultranoc