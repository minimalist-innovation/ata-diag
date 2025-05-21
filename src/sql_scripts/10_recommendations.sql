CREATE TABLE IF NOT EXISTS recommendations
(
    metric_id      INTEGER NOT NULL,
    recommendation TEXT    NOT NULL,
    FOREIGN KEY (metric_id) REFERENCES metrics (id),
    PRIMARY KEY (metric_id, recommendation)
);

DELETE
FROM recommendations;

INSERT OR IGNORE INTO recommendations (metric_id, recommendation)
VALUES
-- Net Promoter Score
(1, 'Segment NPS by customer cohorts to identify patterns and improvement areas'),
(1, 'Implement a closed-loop process to follow up with detractors'),
(1, 'Combine NPS with other customer satisfaction metrics for a more complete picture'),
(1, 'Track NPS trends over time rather than focusing solely on absolute numbers'),
(1, 'Conduct regular NPS surveys at consistent touchpoints in the customer journey'),

-- Customer Satisfaction Score (CSAT)
(2, 'Implement CSAT surveys at critical touchpoints like onboarding and support interactions'),
(2, 'Keep CSAT surveys short and focused to improve response rates'),
(2, 'Use open-ended questions alongside ratings to gather qualitative feedback'),
(2, 'Act quickly on negative CSAT feedback to demonstrate responsiveness'),
(2, 'Track CSAT by product feature to identify areas needing improvement'),

-- % of Roadmap Delivered Quarterly
(3, 'Break large initiatives into smaller, measurable deliverables'),
(3, 'Establish a quarterly review cadence to assess roadmap delivery effectiveness'),
(3, 'Implement clear acceptance criteria for roadmap items'),
(3, 'Maintain a balanced mix of feature work, technical debt, and innovation'),
(3, 'Create delivery quarters for significant milestones as seen in product roadmap best practices'),

-- Average Release Cycle Time
(4, 'Implement continuous integration and automated testing to reduce release friction'),
(4, 'Break down large releases into smaller, more manageable deployments'),
(4, 'Standardize deployment processes to reduce variability in release times'),
(4, 'Track and analyze bottlenecks in the release pipeline'),
(4, 'Balance speed with quality using appropriate testing strategies'),

-- % of Users 'Very Disappointed' if Product is Removed
(5, 'Survey different user segments to identify core value propositions'),
(5, 'Focus product development on features that reduce this percentage'),
(5, 'Target at least 40% "very disappointed" users for strong product-market fit'),
(5, 'Compare this metric across different customer segments to find patterns'),
(5, 'Regularly reassess to ensure continued product-market fit'),

-- % of Features Used by >50% of Users
(6, 'Remove or revise features with consistently low usage rates'),
(6, 'Analyze why high-usage features are successful and apply these learnings'),
(6, 'Improve onboarding to highlight underutilized but valuable features'),
(6, 'Consider moving niche features to premium tiers or add-ons'),
(6, 'Regularly audit feature usage to guide development priorities'),

-- Customer Retention Rate (CRR)
(7, 'Implement an early warning system to identify at-risk customers'),
(7, 'Create customer success programs focused on value realization'),
(7, 'Analyze patterns in churn to identify and address root causes'),
(7, 'Develop targeted retention strategies for different customer segments'),
(7, 'Establish a formal customer feedback loop that informs product development'),

-- Monthly Churn Rate
(8, 'Segment churn by customer tenure, size, and use case to identify hidden patterns'),
(8, 'Remember early success can create "beachhead blindness" with artificially low churn'),
(8, 'Create proactive retention programs for at-risk customer segments'),
(8, 'Focus on first 90-day experience to reduce early churn'),
(8, 'Use the formula: (Customers Lost in Month ÷ Total Customers at Start of Month) × 100%'),

-- Net Revenue Retention (NRR)
(9, 'Implement customer success programs that focus on expansion opportunities'),
(9, 'Identify upsell and cross-sell opportunities through usage analysis'),
(9, 'Create a clear product tiering strategy that encourages upgrades'),
(9, 'Regularly review pricing and packaging to maximize customer lifetime value'),
(9, 'Monitor contraction revenue alongside expansion to get a complete picture'),

-- Annual Recurring Revenue (ARR)
(10, 'Set ARR growth targets broken down by acquisition, expansion, and retention'),
(10, 'Track ARR velocity alongside absolute numbers to measure momentum'),
(10, 'Analyze ARR by customer segment to identify growth opportunities'),
(10, 'Implement forecasting models that account for seasonality and market trends'),
(10, 'Create a balanced growth strategy across new customer acquisition and existing customer expansion'),

-- Monthly Recurring Revenue (MRR)
(11, 'Track MRR changes by category: new, expansion, contraction, and churn'),
(11, 'Analyze MRR trends to identify seasonal patterns and adjust strategies'),
(11, 'Create MRR forecasts that account for sales pipeline and renewal risk'),
(11, 'Set specific MRR targets for different product tiers and customer segments'),
(11, 'Use cohort analysis to understand how MRR evolves over customer lifetime'),

-- Branded Search Traffic
(12, 'Track branded search volume against marketing campaigns to measure effectiveness'),
(12, 'Compare branded vs. non-branded search traffic to assess brand strength'),
(12, 'Optimize landing pages for branded search terms to maximize conversion'),
(12, 'Monitor competitors'' branded search traffic to understand market position'),
(12, 'Use branded search trends to evaluate overall market awareness strategies'),

-- Unaided Brand Recall
(13, 'Conduct regular brand recall surveys in target market segments'),
(13, 'Compare unaided recall against competitors to benchmark performance'),
(13, 'Connect brand recall metrics to broader marketing KPIs to measure effectiveness'),
(13, 'Invest in distinctive brand assets that improve memorability'),
(13, 'Segment brand recall by customer vs. non-customer to assess market penetration'),

-- Gross Margin
(14, 'Regularly audit and optimize infrastructure costs to improve margins'),
(14, 'Implement cost allocation analysis to identify inefficient services'),
(14, 'Consider strategic price increases for low-margin products or services'),
(14, 'Develop automation to reduce manual service costs'),
(14, 'Track gross margin trends by product and customer segment'),

-- LTV:CAC Ratio
(15, 'Target a minimum LTV:CAC ratio of 3:1 for sustainable growth'),
(15, 'Segment LTV:CAC by acquisition channel to optimize marketing spend'),
(15, 'Work to extend customer lifespan through engagement and retention programs'),
(15, 'Reduce CAC through referral programs and organic acquisition strategies'),
(15, 'Increase LTV through strategic upselling and cross-selling initiatives'),

-- Percentage of Features with Clear Monetization Path
(16, 'Map each feature to a specific pricing tier or revenue stream'),
(16, 'Create value-based pricing models tied to measurable customer outcomes'),
(16, 'Develop a framework for evaluating monetization potential during feature planning'),
(16, 'Regularly audit feature usage against revenue contribution'),
(16, 'Test different packaging strategies to optimize feature monetization'),

-- Customer Acquisition Cost (CAC) Payback Period
(17, 'Target industry-specific CAC payback benchmarks (typically 12-18 months for SaaS)'),
(17, 'Improve onboarding to accelerate time-to-value and reduce payback period'),
(17, 'Segment CAC payback by customer size and acquisition channel'),
(17, 'Implement pilot/trial programs that reduce initial acquisition costs'),
(17, 'Balance growth speed with sustainable CAC levels'),

-- Net Dollar Retention (NDR)
(18, 'Set NDR targets by customer segment and tenure'),
(18, 'Implement tiered success programs focused on expansion for key accounts'),
(18, 'Create early warning systems for at-risk revenue'),
(18, 'Develop a systematic approach to price increases and tier upgrades'),
(18, 'Monitor competitive displacement risk in key accounts'),

-- ARR Growth Rate (YoY)
(19, 'Set balanced growth targets across new acquisition and existing customer expansion'),
(19, 'Break down ARR growth rate by customer segment and product line'),
(19, 'Compare ARR growth to market and competitor benchmarks'),
(19, 'Implement a sales capacity model aligned with ARR growth targets'),
(19, 'Create scenario planning models for different growth trajectories'),

-- MRR Growth Rate (MoM)
(20, 'Track MRR growth trends to identify acceleration or deceleration early'),
(20, 'Analyze monthly growth rate volatility to assess business stability'),
(20, 'Segment MRR growth by channel and customer type to identify optimal focus areas'),
(20, 'Balance growth investments against cash conservation needs'),
(20, 'Create rolling 3-month MRR growth forecasts to improve predictability'),

-- % Revenue from Upsell
(21, 'Create clear upgrade paths with tangible value propositions'),
(21, 'Implement usage-based triggers to identify upsell opportunities'),
(21, 'Train customer success teams on effective upsell conversations'),
(21, 'Develop data-driven models to predict upsell readiness'),
(21, 'Test different upsell timing and approaches to optimize conversion'),

-- % Revenue from Cross-sell
(22, 'Map product complementarities to identify cross-sell opportunities'),
(22, 'Develop bundle pricing strategies that encourage multi-product adoption'),
(22, 'Create integrated user experiences across product lines'),
(22, 'Train sales teams on effective cross-selling techniques'),
(22, 'Monitor product adoption sequences to inform cross-sell strategies'),

-- Net Burn Rate
(23, 'Establish burn rate thresholds tied to runway preservation goals'),
(23, 'Create detailed cash flow forecasts with multiple growth scenarios'),
(23, 'Implement regular spend reviews focused on ROI assessment'),
(23, 'Align burn rate with fundraising timeline and milestones'),
(23, 'Track burn rate against growth metrics to ensure efficient capital deployment'),

-- Burn Multiple
(24, 'Target industry-standard burn multiple benchmarks based on growth stage'),
(24, 'Compare burn multiple across time periods to assess capital efficiency trends'),
(24, 'Use burn multiple to evaluate new growth initiatives'),
(24, 'Balance burn multiple optimization with strategic investment needs'),
(24, 'Break down burn multiple by department to identify efficiency opportunities'),

-- Annual Recurring Revenue (ARR) per Employee / Revenue Efficiency
(25, 'Benchmark ARR per employee against industry standards for your growth stage'),
(25, 'Analyze ARR per employee trends as organization scales'),
(25, 'Create department-specific productivity metrics aligned with ARR per employee'),
(25, 'Implement automation and process optimization to improve this ratio'),
(25, 'Use this metric to inform hiring plans and organizational design'),

-- Earnings Before Interest, Taxes, Depreciation & Amortization (EBITDA)
(26, 'Create detailed EBITDA bridges to understand drivers of change'),
(26, 'Develop forecasting models that connect operational metrics to EBITDA impact'),
(26, 'Establish department-level EBITDA contribution targets'),
(26, 'Implement regular variance analysis against EBITDA forecasts'),
(26, 'Balance EBITDA goals with strategic investment needs'),

-- EBITDA Margin
(27, 'Set progressive EBITDA margin targets based on company maturity'),
(27, 'Benchmark EBITDA margins against public company comparables'),
(27, 'Implement cost optimization programs focused on margin improvement'),
(27, 'Balance margin targets with growth investments'),
(27, 'Analyze margin trends across different parts of the business'),

-- Compound Annual Growth Rate (CAGR)
(28, 'Use CAGR to set realistic long-term growth targets'),
(28, 'Compare CAGR across different metrics to ensure balanced growth'),
(28, 'Analyze CAGR by product line and customer segment'),
(28, 'Implement rolling CAGR calculations to identify trends earlier'),
(28, 'Benchmark CAGR against market and competitor growth rates'),

-- The Rule Of 40
(29, 'Target Rule of 40 outcomes appropriate for your growth stage'),
(29, 'Balance the growth vs. profitability mix based on market conditions'),
(29, 'Use Rule of 40 to evaluate strategic initiatives and investments'),
(29, 'Benchmark your Rule of 40 performance against industry peers'),
(29, 'Create glide path models showing the trajectory to Rule of 40 targets'),

-- Percentage of Unused Features Over 90 days
(30, 'Implement feature-level usage tracking to accurately measure adoption'),
(30, 'Create reactivation campaigns for valuable but underutilized features'),
(30, 'Consider removing features with consistently low usage (under 5% in 90 days)'),
(30, 'Improve onboarding to highlight high-value features'),
(30, 'Assess whether unused features are targeting the wrong user segments'),

-- Percentage of Roadmap Influenced by Data
(31, 'Implement a structured framework for incorporating data into roadmap decisions'),
(31, 'Balance data-driven and vision-driven product development'),
(31, 'Create feedback loops that systematically gather customer input'),
(31, 'Develop clear documentation of data sources influencing each roadmap decision'),
(31, 'Train product managers on effective data analysis for decision-making'),

-- The Ratio of GTM Spend to New ARR
(32, 'Benchmark GTM spend ratio against companies at similar growth stages'),
(32, 'Break down spend efficiency by marketing channel and sales segment'),
(32, 'Implement attribution modeling to understand conversion impacts'),
(32, 'Test different GTM investment mixes to optimize returns'),
(32, 'Create cohorted views of GTM efficiency over time'),

-- Cost of Goods Sold COGS as a Percentage Of Revenue
(33, 'Implement regular infrastructure optimization reviews'),
(33, 'Negotiate volume-based discounts with key vendors'),
(33, 'Develop automation to reduce manual service delivery costs'),
(33, 'Analyze COGS by product and customer segment'),
(33, 'Create COGS forecasting models tied to scaling expectations'),

-- Percentage of Strategic Changes Driven by Data
(34, 'Implement a documented decision framework that incorporates data analysis'),
(34, 'Create post-mortem processes that evaluate the quality of data-driven decisions'),
(34, 'Build data literacy across leadership teams'),
(34, 'Balance data insights with market expertise and vision'),
(34, 'Develop clear standards for what constitutes sufficient data for decision-making'),

-- Percentage of Engineering Time on Rework
(35, 'Implement code quality metrics and peer review processes'),
(35, 'Create definition of done standards that reduce subsequent rework'),
(35, 'Analyze patterns in rework to identify systemic issues'),
(35, 'Invest in automated testing to catch issues earlier'),
(35, 'Balance velocity with quality in sprint planning'),

-- Percentage of KPIs with Real-time Visibility
(36, 'Prioritize real-time visibility for operational vs. strategic metrics'),
(36, 'Implement dashboard solutions with appropriate refresh frequencies (<1s for operations, <5m for analytics)'),
(36, 'Define alerting thresholds for critical real-time metrics'),
(36, 'Create backup data access methods for critical systems'),
(36, 'Balance investment in real-time capabilities against other priorities'),

-- Funnel Analytics Completeness
(37, 'Map the entire customer journey and ensure tracking at each stage'),
(37, 'Implement data quality checks to validate funnel data accuracy'),
(37, 'Create cross-functional alignment on funnel definitions and metrics'),
(37, 'Develop attribution models that connect funnel stages'),
(37, 'Regularly audit and update funnel analytics as the business evolves'),

-- Average Time to Close Tickets (ops/dev)
(38, 'Implement SLA targets based on ticket priority and type'),
(38, 'Analyze patterns in resolution time to identify process improvements'),
(38, 'Create escalation paths for tickets exceeding target resolution times'),
(38, 'Balance resolution speed with solution quality'),
(38, 'Track ticket volume and close time by category to identify problem areas'),

-- Average Number of Priorities Per Team Per Sprint
(39, 'Implement work-in-progress (WIP) limits to prevent overcommitment'),
(39, 'Create clear priority tiers for work items'),
(39, 'Track completion rate against commitments to calibrate planning'),
(39, 'Analyze the correlation between focus and delivery quality'),
(39, 'Develop capacity planning models based on historical velocity'),

-- Percentage Revenue From Non-founder Deals
(40, 'Create clear sales playbooks to enable team selling'),
(40, 'Implement graduated founder involvement based on deal stage and size'),
(40, 'Track founder time allocation across sales activities'),
(40, 'Develop specialized sales roles for different customer segments'),
(40, 'Create metrics to evaluate sales team independence and effectiveness'),

-- System Uptime
(41, 'Implement redundancy for critical system components with AWS targets of 99.9% availability'),
(41, 'Create incident response protocols with clear ownership'),
(41, 'Develop preventative maintenance schedules to reduce unplanned downtime'),
(41, 'Implement progressive roll-out strategies to minimize risk'),
(41, 'Create transparent uptime reporting for customers and stakeholders'),

-- Latency Under Load
(42, 'Implement performance budgets for new features focusing on P95 and P99 percentiles'),
(42, 'Create automated performance testing as part of the release process'),
(42, 'Monitor latency across different geographic regions and network conditions'),
(42, 'Analyze correlation between latency and user engagement metrics'),
(42, 'Implement caching and optimization strategies for high-traffic components'),

-- Data Coverage Ratio
(43, 'Create a data integration roadmap prioritizing critical systems'),
(43, 'Implement data quality validation for systems connected to the SSOT'),
(43, 'Develop clear data ownership and governance models'),
(43, 'Create documentation of data flows between systems'),
(43, 'Regularly audit synchronization effectiveness between systems'),

-- User Adoption Rate
(44, 'Target users querying the SSOT at least twice weekly for effective utilization'),
(44, 'Create intuitive interfaces and self-service capabilities'),
(44, 'Track and address barriers to SSOT adoption'),
(44, 'Develop use case examples that demonstrate SSOT value'),
(44, 'Implement champions programs to promote adoption'),

-- Decision Consistency Score
(45, 'Create standardized analysis methodologies for common business questions'),
(45, 'Implement data dictionaries and clear metric definitions'),
(45, 'Develop training programs on consistent data interpretation'),
(45, 'Track and address instances of conflicting analyses from identical data'),
(45, 'Create cross-functional alignment on key business metrics'),

-- Percentage Strategic Founder Time
(46, 'Implement time tracking to measure allocation across strategic activities'),
(46, 'Create delegate structures to reduce operational demands on founders'),
(46, 'Focus on long-term initiatives like market positioning and product roadmaps'),
(46, 'Schedule dedicated strategic thinking time for founders'),
(46, 'Regularly reassess founder involvement across business functions'),

-- Percentage Operational Founder Time
(47, 'Create systems and processes to reduce operational dependencies'),
(47, 'Implement delegation strategies for routine operational tasks'),
(47, 'Hire operational leaders to own day-to-day execution'),
(47, 'Develop clear escalation criteria for when founder involvement is needed'),
(47, 'Track operational time allocation to identify transition opportunities'),

-- Percentage of Team Aligned on Top Three Priorities
(48,
 'Communicate your top three priorities clearly and frequently across multiple channels (emails, meetings, team chats) to reinforce understanding and retention.'),
(48,
 'Connect individual and team tasks to the top three priorities by explaining the "why" behind each assignment, helping everyone see how their work contributes to company goals.'),
(48,
 'Use the "Keep, Cut, Combine" framework to strictly limit your focus to three priorities, eliminating or merging others to avoid dilution of alignment.'),
(48,
 'Hold regular (e.g., weekly) check-ins specifically focused on progress toward the top three priorities, as frequent reviews are proven to increase alignment.'),
(48,
 'Regularly measure and track the percentage of team members who can accurately articulate the top three priorities, using surveys or interviews, to identify alignment gaps and trends.'),
-- Decision Cycle Time (DCT)
(49,
 'Adopt proven decision frameworks like MEDDPICC or RAPID to clarify roles and accelerate decision-making, enabling faster sales qualification and reducing cycle times.'),
(49,
 'Automate manual bottlenecks such as lead scoring and routine approvals to streamline processes and boost efficiency.'),
(49,
 'Create clear, simple partner agreements (SLAs) for B2B2C relationships to prevent external delays and keep cycles predictable.'),
(49,
 'Set up escalation paths for stalled decisions so urgent issues reach executives within 24 hours, maintaining momentum and healthy pipelines.'),
(49,
 'Benchmark and regularly track your Decision Cycle Time against industry standards to identify improvement areas and stay competitive.'),
(49,
 'Use the Cost of Delay framework to prioritize decisions and projects by quantifying the financial impact of waiting, ensuring focus on high-value actions.'),
(49,
 'Balance speed with quality by aiming for appropriate decision velocity-avoid both analysis paralysis and rushed, low-quality choices.'),
(49,
 'Standardize documentation and meeting practices, such as Amazon-style memos and focused reading periods, to ensure clarity and accelerate alignment.'),
(49,
 'Continuously review and refine your decision-making process, learning from delays and iterating to maintain fast, effective execution.'),
-- Lead Conversion Rate from MQL to SQL
(50,
 'Align sales and marketing teams on MQL/SQL definitions using shared CRM dashboards to prevent lead confusion.'),
(50, 'Implement behavioral lead scoring tracking content downloads and product usage patterns.'),
(50, 'Respond to MQLs within one hour to leverage significant conversion increase potential.'),
(50, 'Personalize nurturing campaigns by industry, role, and pain points to boost conversions.'),
(50, 'Use product usage data to identify sales-ready leads in PLG models.'),
(50, 'Prioritize high-quality MQLs over quantity to focus sales efforts effectively.'),
(50, 'Factor sales cycle length into conversion rate timing for accurate measurement.'),
(50, 'Track lead funnel data across CRM and marketing automation tools consistently.'),
(50, 'Analyze conversion rates by lead source to optimize channel investments.'),
(50, 'Establish clear SLA agreements between sales and marketing for lead handoffs.'),
-- Team Engagement Score
(51, 'Conduct monthly engagement pulse checks alongside quarterly eNPS surveys for real-time insights.'),
(51, 'Include open-ended "why" follow-up questions to uncover root causes of engagement gaps.'),
(51, 'Segment scores by department, tenure, and role to identify specific improvement areas.'),
(51, 'Map employee workflows to customer journeys using Service Design principles for alignment.'),
(51, 'Implement recognition programs with budget allocation for spot bonuses and peer shoutouts.'),
(51, 'Create personalized growth plans targeting "Passive" employees to prevent voluntary exits.'),
(51, 'Establish rapid 72-hour response cycles for acting on survey feedback to demonstrate urgency.')
;
