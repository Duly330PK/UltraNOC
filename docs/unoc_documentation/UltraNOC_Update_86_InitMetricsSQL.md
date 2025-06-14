📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📊 UltraNOC – Update 86: init_metrics.sql

## 📂 Pfad

C:\noc_project\UltraNOC\scripts\init_metrics.sql

yaml
Kopieren
Bearbeiten

---

## 📝 Zweck

Initiale Testdaten zur Befüllung der Tabelle `device_metrics`. Diese werden z. B. von der API `/api/v1/metrics/` bereitgestellt und zur Visualisierung oder Testzwecken genutzt.

---

## 🧪 Inhalt (Beispiel)

```sql
INSERT INTO device_metrics (id, device_id, metric_type, value, timestamp)
VALUES
  ('10000000-0000-0000-0000-000000000001', 'core-router-1', 'cpu', 23.4, '2025-06-12T10:00:00Z'),
  ('10000000-0000-0000-0000-000000000002', 'core-router-1', 'mem', 67.8, '2025-06-12T10:00:00Z'),
  ('10000000-0000-0000-0000-000000000003', 'edge-switch-3', 'rx', 8932.2, '2025-06-12T10:05:00Z');
🔧 Voraussetzungen
Tabelle device_metrics muss vor Ausführung existieren (create_metrics_table.py).

UUID-Werte müssen eindeutig sein (können durch uuid_generate_v4() ersetzt werden).

⚙️ Ausführung
bash
Kopieren
Bearbeiten
psql -U root -d ultranoc -f scripts/init_metrics.sql
🛠 Anwendungsfall
Validierung der API /api/v1/metrics/

Beispielinhalt für Frontend-Dashboards oder CLI-Analyse

Seed für Unit- und Integrationstests

© 2025 UltraNOC – Testdatenbereitstellung für Gerätemetriken