CREATE TABLE IF NOT EXISTS industries
(
    id            INTEGER PRIMARY KEY,
    industry_name TEXT NOT NULL UNIQUE
);

DELETE
FROM industries;

INSERT OR IGNORE INTO industries (id, industry_name)
VALUES (1, 'Healthcare'),
       (2, 'Financial Services'),
       (3, 'Retail/E-commerce'),
       (4, 'Manufacturing'),
       (5, 'Construction'),
       (6, 'Logistics/Supply Chain'),
       (7, 'Insurance'),
       (8, 'Hospitality'),
       (9, 'Education'),
       (10, 'Real Estate'),
       (99, 'Other');
