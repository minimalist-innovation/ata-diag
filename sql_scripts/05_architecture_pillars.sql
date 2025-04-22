CREATE TABLE IF NOT EXISTS architecture_pillars
(
    id                       INTEGER PRIMARY KEY,
    architecture_pillar_name TEXT NOT NULL UNIQUE
);

INSERT OR IGNORE INTO architecture_pillars (id, architecture_pillar_name)
VALUES (1, 'Revenue'),
       (2, 'Product'),
       (3, 'Systems'),
       (4, 'People');