CREATE TABLE architecture_pillars
(
    id            INTEGER PRIMARY KEY,
    pillar_name   TEXT    NOT NULL UNIQUE,
    description   TEXT    NOT NULL,
    display_icon  TEXT    NOT NULL,
    display_order INTEGER NOT NULL,
    enabled       INTEGER NOT NULL
);

DELETE
FROM architecture_pillars;

INSERT INTO architecture_pillars
    (id, pillar_name, description, display_icon, display_order, enabled)
VALUES (1, 'Revenue', 'Evaluates acquisition channels and revenue resilience', '💰', 1, TRUE),
       (2, 'Product', 'Assesses product development and market responsiveness', '🎁', 2, TRUE),
       (3, 'Systems', 'Examines operational processes and scalability', '⚙️', 3, TRUE),
       (4, 'People', 'Explores decision-making frameworks and organizational structure', '🧑‍🤝‍🧑', 4, TRUE);
