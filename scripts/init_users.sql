-- C:\noc_project\UltraNOC\scripts\init_users.sql

DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user'
);

-- Admin-Benutzer mit bcrypt-Hash für "admin123"
INSERT INTO users (username, hashed_password, role) VALUES (
    'admin',
    '$2b$12$SZuxF9VX1CzHkxGuYmQaQeZ0HTLbZkeE3BFZq3m08YRWttddjvScC',  -- Passwort: admin123
    'admin'
);
