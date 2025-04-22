CREATE TABLE IF NOT EXISTS saas_types
(
    id        INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL UNIQUE
);

DELETE
FROM saas_types;

INSERT OR IGNORE INTO saas_types (id, type_name)
VALUES (1, 'B2C'),
       (2, 'B2B2C');