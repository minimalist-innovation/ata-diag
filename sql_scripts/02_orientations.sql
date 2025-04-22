CREATE TABLE IF NOT EXISTS orientations
(
    id               INTEGER PRIMARY KEY,
    orientation_name TEXT NOT NULL UNIQUE
);

INSERT OR IGNORE INTO orientations (id, orientation_name)
VALUES (1, 'Horizontal'),
       (2, 'Vertical');
