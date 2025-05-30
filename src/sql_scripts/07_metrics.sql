CREATE TABLE IF NOT EXISTS metrics
(
    id             INTEGER PRIMARY KEY,
    metric_name    TEXT    NOT NULL,
    metric_type_id INTEGER NOT NULL,
    description    TEXT    NOT NULL,
    blog_link      TEXT    NULL,
    video_link     TEXT    NULL,
    units          TEXT    NOT NULL,
    FOREIGN KEY (metric_type_id) REFERENCES metric_types (id)
);

DELETE
FROM metrics;

INSERT OR IGNORE
INTO metrics (id,
              metric_type_id,
              metric_name,
              description,
              blog_link,
              video_link,
              units)
--           PRODUCT PILLAR
VALUES (1,
        3,
        'Net Promoter Score',
        'Net Promoter Score (NPS) measures customer loyalty and likelihood to recommend a product or service, calculated by subtracting the percentage of Detractors (0-6 rating) from Promoters (9-10 rating) on a 0-10 scale. NPS serves as a predictive indicator of business growth potential.',
        'https://www.minimalistinnovation.com/post/csat-nps',
        'https://youtu.be/7403IcyqmPE',
        'Percentage'),
       (2,
        3,
        'Customer Satisfaction Score (CSAT)',
        'Customer Satisfaction Score (CSAT) quantifies customer sentiment by measuring satisfaction with specific interactions, features, or overall experience. Typically collected through surveys using a 1-5 or 1-10 scale, CSAT provides immediate feedback on product performance and service quality.',
        'https://www.minimalistinnovation.com/post/csat-nps',
        'https://youtu.be/7403IcyqmPE',
        'Percentage'),
       (3,
        3,
        '% of Roadmap Delivered Quarterly',
        'This metric tracks the proportion of planned product features and improvements successfully delivered within each quarter relative to the established roadmap. It measures execution effectiveness, development velocity, and the organization''s ability to meet strategic commitments.',
        'https://www.minimalistinnovation.com/post/percentage-roadmap-delivered-quarterly',
        'https://youtu.be/NRLMHfJAFmo',
        'Percentage'),
       (4,
        3,
        'Average Release Cycle Time',
        'Average Release Cycle Time measures the mean duration between successive software releases, from initiation to deployment. This metric reflects development efficiency, quality control processes, and the organization''s agility in responding to market needs and customer feedback.',
        'https://www.minimalistinnovation.com/post/release-cycle-time',
        'https://youtu.be/afsgz1L8crM',
        'Days'),
       (5,
        3,
        '% of Users ''Very Disappointed'' if Product is Removed',
        'The "% of Users ''Very Disappointed'' if Product is Removed" metric is the percentage of surveyed users who indicate they would be "very disappointed" if they could no longer use a product, serving as a key indicator of product-market fit.',
        'https://www.minimalistinnovation.com/post/very-disappointed-user-metric',
        'https://youtu.be/xpIFfuQCmPE',
        'Percentage'),
       (6,
        3,
        '% of Features Used by >50% of Users',
        'This metric measures the proportion of product features that achieve majority adoption (used by over 50% of the user base). It indicates feature relevance, product-market fit, and development efficiency by revealing which capabilities deliver value to most customers versus those with limited utilization.',
        'https://www.minimalistinnovation.com/post/feature-usage-metric',
        'https://youtu.be/me-A7VFpHa0',
        'Percentage'),
       (7,
        3,
        'Customer Retention Rate (CRR)',
        'Customer Retention Rate (CRR) quantifies the percentage of customers retained over a specific timeframe, excluding new acquisitions. Calculated as ((E-N)/S) × 100, where E represents end-period customers, N represents new customers acquired, and S represents start-period customers.',
        'https://www.minimalistinnovation.com/post/customer-retention-rate',
        'https://youtu.be/MUcjhslef-g',
        'Percentage'),
       (8,
        3,
        'Monthly Churn Rate',
        'Monthly Churn Rate is the percentage of subscribers who cancel recurring services within a month. High churn signals product-market misalignment or competitive weaknesses, necessitating retention strategies.',
        'https://www.minimalistinnovation.com/post/monthly-churn-rate',
        'https://youtu.be/AOydX68dr_c',
        'Percentage'),
       (9,
        3,
        'Net Revenue Retention (NRR)',
        'Net Revenue Retention (NRR) measures a SaaS company''s ability to retain and grow revenue from existing customers over a specific period. Calculated as (current period revenue from existing customers ÷ prior period revenue from same customers) × 100%, NRR captures expansion, contraction, and churn effects.',
        'https://www.minimalistinnovation.com/post/net-revenue-retention',
        'https://youtu.be/gQn2fx1fEOY',
        'Percentage'),
       (10,
        2,
        'Annual Recurring Revenue (ARR)',
        'Annual Recurring Revenue (ARR) is the normalized value of contracted recurring revenue components from term subscriptions calculated on a 12-month basis. ARR excludes one-time fees and typically includes yearly subscription revenue plus upgrades minus downgrades and churn, providing visibility into long-term business health.',
        'https://www.minimalistinnovation.com/post/recurring-revenue',
        'https://youtu.be/PQBrqNgC10E',
        'Percentage'),
       (11,
        2,
        'Monthly Recurring Revenue (MRR)',
        'Monthly Recurring Revenue (MRR) represents the predictable or confirmed revenue generated from all active subscriptions in a given month. It excludes one-time payments, free trials, and temporary discounts, focusing solely on stable, recurring revenue components to facilitate short-term financial planning and performance tracking.',
        'https://www.minimalistinnovation.com/post/recurring-revenue',
        'https://youtu.be/PQBrqNgC10E',
        'Percentage'),
--     REVENUE PILLAR
       (12,
        3,
        'Branded Search Traffic',
        'It refers to website visits originating from search engine queries containing specific brand-related keywords, such as a company’s name, product names, or unique service identifiers.',
        'https://www.minimalistinnovation.com/post/branded-search-traffic-unaided-brand-recall',
        'https://youtu.be/-PKY7sJ8R2s',
        'Percentage'),
       (13,
        3,
        'Unaided Brand Recall',
        'Ask someone "What companies make project management software?" The names they list without any hints? That''s unaided brand recall. It''s the brands that live in people''s heads, ready to be mentioned at a moment''s notice.',
        'https://www.minimalistinnovation.com/post/branded-search-traffic-unaided-brand-recall',
        'https://youtu.be/-PKY7sJ8R2s',
        'Percentage'),
       (14,
        2,
        'Gross Margin',
        'Gross margin measures the percentage of revenue remaining after deducting direct costs of delivering services (COGS). For SaaS companies, this metric reflects operational efficiency in converting revenue to gross profit before accounting for fixed costs like R&D and marketing.',
        'https://www.minimalistinnovation.com/post/gross-margin',
        'https://youtu.be/tKPigwoPyg0',
        'Percentage'),
       (15,
        3,
        'LTV:CAC Ratio',
        'The LTV:CAC ratio quantifies the relationship between the lifetime value (LTV) of a customer and the cost to acquire that customer (CAC).',
        'https://www.minimalistinnovation.com/post/ltv-cac-ratio',
        'https://youtu.be/-XH4mqWXHTY',
        'Percentage'),
       (16,
        3,
        'Percentage of Features with Clear Monetization Path',
        'The "Percentage of Features with Clear Monetization Path" measures how much of your SaaS product drives revenue.',
        'https://www.minimalistinnovation.com/post/feature-monetization-metric',
        'https://youtu.be/JRZ-ozHfxxI',
        'Percentage'),
       (17,
        3,
        'Customer Acquisition Cost (CAC) Payback Period',
        'CAC payback period (CPP) measures how many months it takes to recover what you spent to acquire a customer, after accounting for the costs of serving them.',
        'https://www.minimalistinnovation.com/post/cac-payback-period',
        'https://youtu.be/Z_fW8rijIwk',
        'Months'),
       (18,
        3,
        'Net Dollar Retention',
        'Net Dollar Retention shows how much money a company keeps from its current customers over time.',
        'https://www.minimalistinnovation.com/post/net-dollar-retention',
        'https://youtu.be/pdz7sw2nrRQ',
        'Percentage'),
       (19,
        3,
        'ARR Growth Rate',
        'ARR Growth Rate (YoY) measures the percentage change in ARR over consecutive 12-month periods.',
        'https://www.minimalistinnovation.com/post/arr-mrr-growth-rate',
        'https://youtu.be/VbUtKwDu9UI',
        'Percentage'),
       (20,
        3,
        'MRR Growth Rate',
        'MRR Growth Rate (MoM) measures how quickly your monthly revenue(MRR) is growing, as a percentage.',
        'https://www.minimalistinnovation.com/post/arr-mrr-growth-rate',
        'https://youtu.be/VbUtKwDu9UI',
        'Percentage'),
       (21,
        3,
        '% Revenue from Upsell',
        'Upselling refers to the strategy of encouraging existing customers to upgrade to a higher-tier version of the same product they already use.',
        'https://www.minimalistinnovation.com/post/upsell-crosssell',
        'https://youtu.be/HsoAXZXDM9g',
        'Percentage'),
       (22,
        3,
        '% Revenue from Cross-sell',
        'Cross-selling involves offering additional products or complementary features that supplement the customer''s initial purchase.',
        'https://www.minimalistinnovation.com/post/upsell-crosssell',
        'https://youtu.be/HsoAXZXDM9g',
        'Percentage'),
       (23,
        3,
        'Net Burn Rate',
        'Net Burn Rate measures the rate at which a SaaS company consumes its cash reserves after accounting for revenue generated during the same period. It reflects the net cash loss per month or quarter.',
        'https://www.minimalistinnovation.com/post/net-burn-rate-vs-burn-multiple',
        'https://youtu.be/2KxwMaHO1JE',
        'Currency per period'),
       (24,
        3,
        'Burn Multiple',
        'Burn Multiple quantifies capital efficiency by measuring how much cash a company burns to generate $1 of new Annual Recurring Revenue (ARR).',
        'https://www.minimalistinnovation.com/post/net-burn-rate-vs-burn-multiple',
        'https://youtu.be/2KxwMaHO1JE',
        'Percentage'),
       (25,
        3,
        'Annual Recurring Revenue (ARR) per Employee or Revenue Efficiency',
        'Revenue efficiency in SaaS is quantified as Annual Recurring Revenue (ARR) per employee, a metric that divides a company’s total ARR by its full-time equivalent (FTE) headcount. This ratio measures the average recurring revenue generated per employee, serving as a barometer of operational efficiency and workforce productivity.',
        'https://www.minimalistinnovation.com/post/revenue-efficiency',
        'https://youtu.be/TDZSursOWcE',
        'Currency'),
       (26,
        1,
        'Earnings Before Interest, Taxes, Depreciation & Amortization (EBITDA)',
        'Earnings Before Interest, Taxes, Depreciation & Amortization is a measure of a company''s operational profitability, excluding non-operational expenses and non-cash accounting charges.',
        'https://www.minimalistinnovation.com/post/ebitda-cagr-rule-of-40',
        'https://youtu.be/w-ZKs_JR3J8',
        'Currency'),
       (27,
        2,
        'Earnings Before Interest, Taxes, Depreciation & Amortization (EBITDA) Margin',
        'Shows EBITDA as a percentage of its total revenue.',
        'https://www.minimalistinnovation.com/post/ebitda-cagr-rule-of-40.',
        'https://youtu.be/w-ZKs_JR3J8',
        'Currency'),
       (28,
        3,
        'Compound Annual Growth Rate (CAGR)',
        'Compound Annual Growth Rate is the smoothed annualized growth rate of a metric (e.g., revenue) over a multi-year period, assuming steady growth.',
        'https://www.minimalistinnovation.com/post/ebitda-cagr-rule-of-40',
        'https://youtu.be/w-ZKs_JR3J8',
        'Currency'),
       (29,
        2,
        'The Rule Of 40',
        'Combines EBITDA Margin + Revenue Growth Rate to evaluate the tradeoff between growth and profitability.',
        'https://www.minimalistinnovation.com/post/ebitda-cagr-rule-of-40',
        'https://youtu.be/w-ZKs_JR3J8',
        'Currency'),
       --     SYSTEMS
       (30,
        3,
        'Percentage of Unused Features Over 90 days',
        'Measures features with less than 5% user adoption within a 90-day window.',
        'https://www.minimalistinnovation.com/post/unused-features',
        'https://youtu.be/CQ0Jnv923tM',
        'Percentage'),
       (31,
        3,
        'Percentage of Roadmap Influenced by Data',
        'Quantifies the proportion of  product development initiatives driven by Structured Analysis*. This encompasses any features, updates, or strategic shifts that rely on primary data (including user behavior metrics, customer surveys, and A/B tests) and secondary data (covering market research and competitive analysis).',
        'https://www.minimalistinnovation.com/post/percent-roadmap-influenced-by-data',
        'https://youtu.be/kPwNFmar-vA',
        'Percentage'),
       (32,
        3,
        'The Ratio of GTM Spend to New ARR',
        'Measures the total sales and marketing expenditure required to generate one dollar of net new Annual Recurring Revenue (ARR).',
        'https://www.minimalistinnovation.com/post/gtm-spend-to-new-arr',
        'https://youtu.be/d_N3wWnCvbE',
        'Percentage'),
       (33,
        3,
        'Cost of Goods Sold COGS as a Percentage Of Revenue',
        'Represents a financial ratio that measures what proportion of a company''s revenue is consumed by direct costs required to produce the goods or services sold.',
        'https://www.minimalistinnovation.com/post/slash-saas-cogs',
        'https://youtu.be/BpvnE35w4IE',
        'Percentage'),
       (34,
        3,
        'Percentage of Strategic Changes Driven by Data',
        'Represents the share of high-impact decisions-like product pivots, pricing changes, or market expansions-guided by quantitative analysis, not just gut feel.',
        'https://www.minimalistinnovation.com/post/percent-strategic-changes-driven-by-data',
        'https://youtu.be/w1U4z0Qg-7Y',
        'Percentage'),
       (35,
        3,
        'Percentage of Engineering Time on Rework',
        'Quantifies the proportion of total developer effort - time spent  revising, correcting, or modifying existing code, features, or architecture due to defect resolution, requirement changes or technical debt cleanup.',
        'https://www.minimalistinnovation.com/post/engineering-rework-metrics',
        'https://youtu.be/YW8gQelLuck',
        'Percentage'),
       (36,
        3,
        'Percentage of KPIs with Real-Time Visibility',
        'Represents the proportion of essential business metrics that SaaS startups can monitor and access with near-zero latency. (Forrester defines "real-time" as <1 second for operational KPIs and <5 minutes for analytics.)',
        'https://www.minimalistinnovation.com/post/real-time-kpi-visibility',
        'https://youtu.be/SIuk00u0iTE',
        'Percentage'),
       (37,
        3,
        'Funnel Analytics Completeness',
        'Funnel Analytics Completeness refers to the systematic tracking and analysis of all essential stages, metrics and user interactions across customer acquisition and retention journeys in SaaS models.',
        'https://www.minimalistinnovation.com/post/funnel-analytics-completeness',
        'https://youtu.be/2-9RnPzo_JI',
        'Percentage'),
       (38,
        3,
        'Average Time to Close Tickets (ops/dev)',
        'Average Time to Close Tickets (ops/dev) refers to the average time it takes for operations and development to fully resolve a technical support ticket. This crucial metric—measured from ticket creation to resolution—reflects the efficiency of resolving bugs, launching features, and tackling complex integrations.',
        'https://www.minimalistinnovation.com/post/saas-ticket-resolution',
        'https://youtu.be/BdnQ6muQwos',
        'Hours'),
       (39,
        3,
        'Average Number of Priorities Per Team Per Sprint',
        'Average Number of Priorities Per Team Per Sprint measures how many distinct work items (user stories, bug fixes, technical tasks) your SaaS team commits to and completes in each sprint. This metric reflects both planning accuracy and delivery capability.',
        'https://www.minimalistinnovation.com/post/saas-ticket-resolution',
        'https://youtu.be/jfA_GWz2P8k',
        'Count'),
       (40,
        3,
        'Percentage Revenue From Non-founder Deals',
        'Percentage Revenue From Non-founder Deals quantifies the proportion of a SaaS company''s total revenue generated through channels not directly involving founders in sales or customer acquisition.',
        'https://www.minimalistinnovation.com/post/non-founder-revenue-saas-scaling-success',
        'https://youtu.be/LGjnSe-szGw',
        'Percentage'),
       (41,
        3,
        'Uptime',
        'System Uptime is the percentage of time your app is available and working.',
        'https://www.minimalistinnovation.com/post/saas-uptime-latency',
        'https://youtu.be/0FcMjArymzI',
        'Percentage'),
       (42,
        3,
        'Latency',
        'Latency Under Load is how fast your app responds when lots of users hit it at once.',
        'https://www.minimalistinnovation.com/post/saas-uptime-latency',
        'https://youtu.be/0FcMjArymzI',
        'Milliseconds'),
       (43,
        3,
        'Data Coverage Ratio',
        'Data Coverage Ratio is the percentage of systems both sending and receiving updates from the Single Source of Truth (SSOT), reflecting true integration and comprehensive data synchronization across platforms.',
        'https://www.minimalistinnovation.com/post/single-source-of-truth-adoption-saas',
        'https://youtu.be/ZRVHVIURxsw',
        'Percentage'),
       (44,
        3,
        'User Adoption Rate',
        'User Adoption Rate is the percentage of users querying the Single Source of Truth (SSOT) at least twice weekly, indicating active engagement and effective utilization of the centralized data source.',
        'https://www.minimalistinnovation.com/post/single-source-of-truth-adoption-saas',
        'https://youtu.be/ZRVHVIURxsw',
        'Percentage'),
       (45,
        3,
        'Decision Consistency Score',
        'Decision Consistency Score is the frequency with which teams generate conflicting analyses from identical data, measuring reliability and alignment in data-driven decision-making processes.',
        'https://www.minimalistinnovation.com/post/single-source-of-truth-adoption-saas',
        'https://youtu.be/ZRVHVIURxsw',
        'Percentage'),
       (46,
        3,
        'Percentage Strategic Founder Time',
        'Percentage Strategic Founder Time measures the proportion of total work hours dedicated to long-term initiatives such as market positioning, product roadmaps, partnership development, and scalability planning.',
        'https://www.minimalistinnovation.com/post/saas-founder-time-operations-vs-strategy-burnout',
        'https://youtu.be/ZRVHVIURxsw',
        'Percentage'),
       (47,
        3,
        'Percentage Operational Founder Time',
        'Percentage Operational Founder Time measures the percentage of total team time dedicated to maintaining existing systems, including support, technical debt, feature deployment, and incident response activities.',
        'https://www.minimalistinnovation.com/post/saas-founder-time-operations-vs-strategy-burnout',
        'https://youtu.be/1RC06JgWVYU',
        'Percentage'),
       (48,
        3,
        'Percentage of Team Aligned on Top Three Priorities',
        'Percentage of Team Aligned on Top Three Priorities measures the share of employees in your startup who can clearly identify and articulate the organization''s three most important strategic goals.',
        'https://www.minimalistinnovation.com/post/team-alignment-top-3-priorities',
        'https://youtu.be/KSiPqSDF3wo',
        'Percentage'),
       (49,
        3,
        'Decision Cycle Time (DCT)',
        'Decision Cycle Time (DCT) tracks the complete duration from identifying a decision need to full implementation, mirroring the sales "Time-to-Close" metric.',
        'https://www.minimalistinnovation.com/post/decision-cycle-time',
        'https://youtu.be/trTTxTx5cT4',
        'Days'),
       (50,
        3,
        'Lead Conversion Rate from MQL to SQL',
        'The MQL to SQL Conversion Rate tracks the percentage of marketing-engaged leads that sales deems ready for direct engagement and likely to buy.',
        'https://www.minimalistinnovation.com/post/lead-conversion-rate-mql-to-sql',
        'https://youtu.be/NnpQQthwF9s',
        'Percentage'),
       (51,
        3,
        'Team Engagement Score',
        'Team Engagement Score measures emotional commitment, goal alignment, and willingness to go extra mile, combining survey responses into a single score (0-100).',
        'https://www.minimalistinnovation.com/post/team-happiness-enps-guide',
        'https://youtu.be/0Kv1LGAN0DQ',
        'Percentage'),
       (52,
        3,
        '% of Roles with OKRs',
        'Percentage of Roles with OKRs tracks the job functions with Objectives and Key Results tied to your core strategy. It reveals if OKRs are integrated across all teams or limited to leadership.',
        'https://www.minimalistinnovation.com/post/roles-with-okrs',
        'https://youtu.be/k4n5mJaybk4',
        'Percentage'),
       (53,
        3,
        'Competitive Win Rate',
        'Competitive Win Rate shows the percentage of deals you win against direct competitors, not all deals, in a specific segment when customers compare options.',
        'https://www.minimalistinnovation.com/post/competitive-win-rate',
        'https://youtu.be/e24-f8MJhL8',
        'Percentage'),
       (54,
        3,
        'Span of Control',
        'Span of Control measures how many full-time equivalent employees report to each manager, standardizing staffing levels for organizational comparison and management.',
        'https://www.minimalistinnovation.com/post/fte-per-manager-ratio',
        'https://youtu.be/DX_E3045Pn4',
        'Count');