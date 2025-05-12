CREATE TABLE IF NOT EXISTS growth_stages
(
    id                INTEGER PRIMARY KEY,
    growth_stage_name TEXT           NOT NULL,
    description       TEXT           NOT NULL,
    low_range         DECIMAL(10, 2) NOT NULL,
    high_range        DECIMAL(10, 2) NOT NULL
);

DELETE
FROM growth_stages;

INSERT INTO growth_stages
VALUES (1,
        'Pre-Qualification',
        'Your company is still in early stages (under $1M ARR). While this tool is for more established businesses, we''ve created something specifically for you. Download our <a href="https://minimalistinnovation.com/book">free e-book</a> now to master product-market fit and prepare for your next growth phase.',
        0.00,
        1.00),
       (2,
        'Validation Seekers',
        'Your company is in the Validation Seekers stage ($1M-$2M ARR). At this stage, you''re likely establishing early monetization with some paying customers, but may be encountering your first serious growth plateau or realizing early traction was a false signal.',
        1.01,
        2.00),
       (3,
        'Traction Builders',
        'Your company is in the Traction Builders stage ($2M-$4M ARR). You''ve achieved early validation but may have hit a plateau in growth. You might be experimenting with positioning or pricing pivots without clarity.',
        2.01,
        4.00),
       (4,
        'Scale Preparers',
        'Your company is in the Scale Preparers stage ($4M-$7M ARR). You may be stuck in ''hiring solves everything'' mode, but growth has stalled. You could be questioning whether your initial model can scale or needs a pivot.',
        4.01,
        7.00),
       (5,
        'Growth Accelerators',
        'Your company is in the Growth Accelerators stage ($7M-$10M ARR). You''re likely facing internal chaos from rapid scaling and unclear priorities, and may be unsure if you should push deeper into your core or pivot to a broader opportunity.',
        7.01,
        10.00),
       (6,
        'Expansion Navigators',
        'Your company is in the Expansion Navigators stage ($10M+ ARR). You''re likely reaching the upper bounds of your initial market and expanding into adjacent opportunities.',
        10.01,
        999.99);