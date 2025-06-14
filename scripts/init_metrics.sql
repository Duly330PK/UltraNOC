-- C:\noc_project\UltraNOC\scripts\init_metrics.sql

-- Diese Datei setzt Beispielmetriken für ein Gerät zur Initialisierung

INSERT INTO device_metrics (id, device_id, metric_type, value, timestamp)
VALUES
  (gen_random_uuid(), 'router-001', 'cpu', 34.5, NOW()),
  (gen_random_uuid(), 'router-001', 'mem', 68.2, NOW()),
  (gen_random_uuid(), 'router-001', 'rx', 123.0, NOW()),
  (gen_random_uuid(), 'router-001', 'tx', 98.7, NOW());
