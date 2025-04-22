CREATE TABLE architecture_pillars
(
    id            INTEGER PRIMARY KEY,
    pillar_name   TEXT    NOT NULL UNIQUE,
    description   TEXT    NOT NULL,
    display_order INTEGER NOT NULL
);

DELETE
FROM architecture_pillars;

INSERT INTO architecture_pillars
    (id, pillar_name, description, display_order)
VALUES (1, 'Revenue', 'Evaluates acquisition channels and revenue resilience', 1),
       (2, 'Product', 'Assesses product development and market responsiveness', 2),
       (3, 'Systems', 'Examines operational processes and scalability', 3),
       (4, 'People', 'Explores decision-making frameworks and organizational structure', 4);
