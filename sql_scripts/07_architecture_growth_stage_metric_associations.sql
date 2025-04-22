CREATE TABLE IF NOT EXISTS architecture_growth_stage_metric_associations
(
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    growth_stage_id        INTEGER NOT NULL,
    architecture_pillar_id INTEGER NOT NULL,
    saas_type_id                   NULL,
    industry_id                    NULL,
    metric_id                      NOT NULL,
    FOREIGN KEY (growth_stage_id) REFERENCES growth_stages (id),
    FOREIGN KEY (architecture_pillar_id) REFERENCES architecture_pillars (id),
    FOREIGN KEY (saas_type_id) REFERENCES sass_types (id),
    FOREIGN KEY (industry_id) REFERENCES industries (id),
    FOREIGN KEY (metric_id) REFERENCES metrics (id)
);

CREATE INDEX IF NOT EXISTS idx_architecture_growth_stage_metric_associations
    ON architecture_growth_stage_metric_associations (architecture_pillar_id, growth_stage_id, metric_id);