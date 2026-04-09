-- Drop if exists for clean restarts during dev
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id                  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name                VARCHAR(100),
    age                 INTEGER,
    promotion_score     NUMERIC(10,2),
    loaded_at           TIMESTAMP DEFAULT NOW()
);


