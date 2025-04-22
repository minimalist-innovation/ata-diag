CREATE TABLE IF NOT EXISTS architecture_growth_stage_metric_associations
(
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    architecture_pillar_id INTEGER NOT NULL,
    growth_stage_id        INTEGER NOT NULL,
    metric_id                      NOT NULL,
    FOREIGN KEY (id) REFERENCES architecture_pillars (id),
    FOREIGN KEY (growth_stage_id) REFERENCES growth_stages (id),
    FOREIGN KEY (metric_id) REFERENCES metrics (id)
);

CREATE INDEX IF NOT EXISTS idx_architecture_growth_stage_metric_associations
    ON architecture_growth_stage_metric_associations (architecture_pillar_id, growth_stage_id, metric_id);