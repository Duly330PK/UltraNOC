📝 Dokumentation – update_63_requirements_txt.md
📁 Pfad: C:\noc_project\UltraNOC\docs\updates\update_63_requirements_txt.md

📄 Quelltext:

markdown
Kopieren
Bearbeiten
# 📦 Update 63 – Abhängigkeiten backend-seitig (requirements.txt)

## Ziel
Konsolidierung aller notwendigen Backend-Abhängigkeiten für den Betrieb und die Entwicklung der UltraNOC-Plattform.

## Datei
📄 `C:\noc_project\UltraNOC\backend\requirements.txt`

## Inhalt (aktualisiert)

```text
fastapi==0.110.0
uvicorn[standard]==0.29.0
SQLAlchemy==1.4.49
psycopg2-binary==2.9.9
python-dotenv==1.0.1
passlib[bcrypt]==1.7.4
python-jose==3.3.0
pydantic==2.7.1
pytest==8.2.2
httpx==0.27.0
Änderungen gegenüber vorheriger Version
Paket	Status	Kommentar
pydantic	⬆️ aktualisiert	v2 benötigt für from_attributes
python-dotenv	✅ übernommen	Für Umgebungsvariablen (.env)
passlib[bcrypt]	✅ übernommen	Für sichere Passwort-Hashing-Logik
python-jose	✅ übernommen	JWT-Erstellung & -Verifikation
pytest	➕ neu	Testframework für Auth- & API-Tests
httpx	➕ neu	Optionale Tests / Clientsimulationen

Hinweise
Diese Datei ist ausschließlich für das Backend bestimmt.

Frontend-Abhängigkeiten werden separat über package.json verwaltet.