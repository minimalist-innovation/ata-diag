CREATE TABLE IF NOT EXISTS industry_mappings
(
    saas_type_id   INTEGER NOT NULL,
    orientation_id INTEGER NOT NULL,
    industry_id    INTEGER NOT NULL,
    PRIMARY KEY (saas_type_id, orientation_id, industry_id),
    FOREIGN KEY (saas_type_id) REFERENCES saas_types (id),
    FOREIGN KEY (orientation_id) REFERENCES orientations (id),
    FOREIGN KEY (industry_id) REFERENCES industries (id)
);

DELETE
FROM industry_mappings;

INSERT OR IGNORE INTO industry_mappings
VALUES (1, 2, 1),
       (1, 2, 2),
       (1, 2, 3),
       (1, 2, 9),
       (1, 1, 4),
       (1, 1, 5),
       (1, 1, 6),
       (2, 2, 7),
       (2, 2, 8),
       (2, 2, 10),
       (2, 1, 1),
       (2, 1, 2),
       (1, 1, 99),
       (1, 2, 99),
       (2, 1, 99),
       (2, 2, 99); -- Other
