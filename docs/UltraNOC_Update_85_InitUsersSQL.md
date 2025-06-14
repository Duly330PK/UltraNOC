📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 👤 UltraNOC – Update 85: init_users.sql

## 📂 Pfad

C:\noc_project\UltraNOC\scripts\init_users.sql

yaml
Kopieren
Bearbeiten

---

## 📝 Zweck

Dieses SQL-Skript dient zur Initialbefüllung der `users`-Tabelle in PostgreSQL mit vordefinierten Benutzerkonten – insbesondere dem `admin`-Nutzer für Authentifizierungstests.

---

## 🧪 Inhalt (Beispiel)

```sql
INSERT INTO users (id, username, hashed_password, role)
VALUES (
  '00000000-0000-0000-0000-000000000001',
  'admin',
  '$2b$12$Vz5tUzZT9UO0jQ8Lhzjq9OP9Xzj7ZbxzUtMPVL2urN.eIdhv7PBXK',  -- bcrypt: admin123
  'admin'
);
🔐 Hinweis
Das Passwort admin123 wurde mit bcrypt gehasht (passlib).

Die id ist als UUID gesetzt und eindeutig.

Die Rolle ist admin, um Zugriff auf geschützte Endpunkte zu ermöglichen.

📦 Anwendung
bash
Kopieren
Bearbeiten
psql -U root -d ultranoc -f scripts/init_users.sql
📋 Voraussetzung
Die users-Tabelle muss zuvor mittels SQLAlchemy oder init.sql erstellt worden sein.

© 2025 UltraNOC – Benutzerinitialisierung für Authentifizierungstests