CREATE TABLE IF NOT EXISTS metric_types
(
    id        INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL UNIQUE
);

DELETE
FROM metric_types;

INSERT OR IGNORE INTO metric_types (id, type_name)
VALUES (1, 'INPUT'),
       (2, 'CALCULATED'),
       (3, 'BENCHMARK');