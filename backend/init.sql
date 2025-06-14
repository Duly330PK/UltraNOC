-- C:\noc_project\UltraNOC\scripts\init_users.sql

-- Erfordert PostgreSQL-Erweiterung pgcrypto für UUID-Generierung
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Initialer Admin-Nutzer
INSERT INTO users (id, username, hashed_password, role)
VALUES (
  gen_random_uuid(),
  'admin',
  '$2b$12$wXGc2kSmYZc9qT5ZT1k5NexX9JRy2RLNbdvKkhUtU3GnAZkBDxFRG',
  'admin'
);
