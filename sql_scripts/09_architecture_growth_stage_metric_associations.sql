CREATE TABLE IF NOT EXISTS architecture_growth_stage_metric_associations
(
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    growth_stage_id        INTEGER        NOT NULL,
    architecture_pillar_id INTEGER        NOT NULL,
    saas_type_id                          NULL,
    industry_id                           NULL,
    metric_id                             NOT NULL,
    min_value              DECIMAL(10, 2) NOT NULL,
    max_value              DECIMAL(10, 2) NOT NULL,
    lo_range_value         DECIMAL(10, 2) NOT NULL,
    hi_range_value         DECIMAL(10, 2) NOT NULL,
    metric_enabled         BOOLEAN        NOT NULL CHECK (metric_enabled IN (0,1)),
    key_takeaways          TEXT           NOT NULL,
    FOREIGN KEY (growth_stage_id) REFERENCES growth_stages (id),
    FOREIGN KEY (architecture_pillar_id) REFERENCES architecture_pillars (id),
    FOREIGN KEY (saas_type_id) REFERENCES saas_types (id),
    FOREIGN KEY (industry_id) REFERENCES industries (id),
    FOREIGN KEY (metric_id) REFERENCES metrics (id)
);

CREATE INDEX IF NOT EXISTS idx_architecture_growth_stage_metric_associations
    ON architecture_growth_stage_metric_associations (architecture_pillar_id, growth_stage_id, metric_id);

DELETE
FROM architecture_growth_stage_metric_associations;

INSERT INTO architecture_growth_stage_metric_associations(id,
                                                          growth_stage_id,
                                                          architecture_pillar_id,
                                                          saas_type_id,
                                                          industry_id,
                                                          metric_id,
                                                          min_value,
                                                          max_value,
                                                          lo_range_value,
                                                          hi_range_value,
                                                          metric_enabled,
                                                          key_takeaways)
VALUES 
(1,  2, 2, NULL, NULL, 1, 0, 100, 20, 35, 1, "Time your NPS check-ins right : Send surveys 2–3 months after core value delivery to get meaningful feedback. Segment and spot early warning signs : Analyze NPS by segment to catch declining trends before renewals. Link feedback to usage : Compare promoter vs. detractor behavior to uncover actionable product insights. Act fast on feedback : Celebrate promoters, request referrals, and route scores to CRM for visibility and follow-up."),
(2,  3, 2, NULL, NULL, 1, 0, 100, 35, 50, 1, "Time your NPS check-ins right : Send surveys 2–3 months after core value delivery to get meaningful feedback. Segment and spot early warning signs : Analyze NPS by segment to catch declining trends before renewals. Link feedback to usage : Compare promoter vs. detractor behavior to uncover actionable product insights. Act fast on feedback : Celebrate promoters, request referrals, and route scores to CRM for visibility and follow-up."),
(3,  4, 2, NULL, NULL, 1, 0, 100, 50, 65, 1, "Time your NPS check-ins right : Send surveys 2–3 months after core value delivery to get meaningful feedback. Segment and spot early warning signs : Analyze NPS by segment to catch declining trends before renewals. Link feedback to usage : Compare promoter vs. detractor behavior to uncover actionable product insights. Act fast on feedback : Celebrate promoters, request referrals, and route scores to CRM for visibility and follow-up."),
(4,  5, 2, NULL, NULL, 1, 0, 100, 60, 75, 1, "Time your NPS check-ins right : Send surveys 2–3 months after core value delivery to get meaningful feedback. Segment and spot early warning signs : Analyze NPS by segment to catch declining trends before renewals. Link feedback to usage : Compare promoter vs. detractor behavior to uncover actionable product insights. Act fast on feedback : Celebrate promoters, request referrals, and route scores to CRM for visibility and follow-up."),
(5,  2, 2, NULL, NULL, 2, 0, 100, 65, 80, 1, "Check CSAT right after key moments : Smooth out onboarding bumps. Segment to spot patterns : Break down results by plan, persona, and usage to identify trends. Fix what bugs your users, and obvious product bugs! Tie CSAT to actions : Investigate low scores by tracing them back to specific failed steps.        
Keep your fans happy. Respond quickly : Turn feedback into systematic growth."),
(6,  3, 2, NULL, NULL, 2, 0, 100, 75, 85, 1, "Check CSAT right after key moments : Smooth out onboarding bumps. Segment to spot patterns : Break down results by plan, persona, and usage to identify trends. Fix what bugs your users, and obvious product bugs! Tie CSAT to actions : Investigate low scores by tracing them back to specific failed steps.        
Keep your fans happy. Respond quickly : Turn feedback into systematic growth."),
(7,  4, 2, NULL, NULL, 2, 0, 100, 85, 92, 1, "Check CSAT right after key moments : Smooth out onboarding bumps. Segment to spot patterns : Break down results by plan, persona, and usage to identify trends. Fix what bugs your users, and obvious product bugs! Tie CSAT to actions : Investigate low scores by tracing them back to specific failed steps.        
Keep your fans happy. Respond quickly : Turn feedback into systematic growth."),
(8,  5, 2, NULL, NULL, 2, 0, 100, 90, 95, 1, "Check CSAT right after key moments : Smooth out onboarding bumps. Segment to spot patterns : Break down results by plan, persona, and usage to identify trends. Fix what bugs your users, and obvious product bugs! Tie CSAT to actions : Investigate low scores by tracing them back to specific failed steps.        
Keep your fans happy. Respond quickly : Turn feedback into systematic growth."),
(9,  2, 2, 1,    NULL, 4, 0, 60,   3,  5, 1, "Break big features into bite-sized parts : If it takes over two days, it's too big; think in microservices and modular components. Cut delays and trust your team : Remove bottlenecks like long approvals and slow code reviews; empower fast, autonomous action. Automate relentlessly : Let machines handle repetitive tasks using CI/CD tools to save time and reduce errors."),
(10, 2, 2, 2,    NULL, 4, 0, 60,   7,  8, 1, "Break big features into bite-sized parts : If it takes over two days, it's too big; think in microservices and modular components. Cut delays and trust your team : Remove bottlenecks like long approvals and slow code reviews; empower fast, autonomous action. Automate relentlessly : Let machines handle repetitive tasks using CI/CD tools to save time and reduce errors."),
(11, 3, 2, 1,    NULL, 4, 0, 60,   5,  8, 1, "Break big features into bite-sized parts : If it takes over two days, it's too big; think in microservices and modular components. Cut delays and trust your team : Remove bottlenecks like long approvals and slow code reviews; empower fast, autonomous action. Automate relentlessly : Let machines handle repetitive tasks using CI/CD tools to save time and reduce errors."),
(12, 3, 2, 2,    NULL, 4, 0, 60,  10, 14, 1, "Break big features into bite-sized parts : If it takes over two days, it's too big; think in microservices and modular components. Cut delays and trust your team : Remove bottlenecks like long approvals and slow code reviews; empower fast, autonomous action. Automate relentlessly : Let machines handle repetitive tasks using CI/CD tools to save time and reduce errors."),
(13, 4, 2, 1,    NULL, 4, 0, 60,   7, 12, 1, "Break big features into bite-sized parts : If it takes over two days, it's too big; think in microservices and modular components. Cut delays and trust your team : Remove bottlenecks like long approvals and slow code reviews; empower fast, autonomous action. Automate relentlessly : Let machines handle repetitive tasks using CI/CD tools to save time and reduce errors."),
(14, 4, 2, 2,    NULL, 4, 0, 60,  12, 18, 1, "Break big features into bite-sized parts : If it takes over two days, it's too big; think in microservices and modular components. Cut delays and trust your team : Remove bottlenecks like long approvals and slow code reviews; empower fast, autonomous action. Automate relentlessly : Let machines handle repetitive tasks using CI/CD tools to save time and reduce errors."),
(15, 5, 2, 1,    NULL, 4, 0, 60,  10, 14, 1, "Break big features into bite-sized parts : If it takes over two days, it's too big; think in microservices and modular components. Cut delays and trust your team : Remove bottlenecks like long approvals and slow code reviews; empower fast, autonomous action. Automate relentlessly : Let machines handle repetitive tasks using CI/CD tools to save time and reduce errors."),
(16, 5, 2, 2,    NULL, 4, 0, 60,  14, 21, 1, "Break big features into bite-sized parts : If it takes over two days, it's too big; think in microservices and modular components. Cut delays and trust your team : Remove bottlenecks like long approvals and slow code reviews; empower fast, autonomous action. Automate relentlessly : Let machines handle repetitive tasks using CI/CD tools to save time and reduce errors."),
(17, 2, 2, 1,    NULL, 3, 0, 100,  60, 100, 1, "Fix what frustrates users : Focus on real pain points, not 'cool' ideas. Bet mostly on what's proven : Spend 70% on sure wins, 30% on bold bets. Only build what matters : Ship features that drive value, virality, or stickiness. Measure impact, not activity : Prioritize real user outcomes over just hitting deadlines. Align the whole team : Ensure every function shares the same goals and roadmap clarity."),
(18, 2, 2, 2,    NULL, 3, 0, 100,  50, 100, 1, "Fix what frustrates users : Focus on real pain points, not 'cool' ideas. Bet mostly on what's proven : Spend 70% on sure wins, 30% on bold bets. Only build what matters : Ship features that drive value, virality, or stickiness. Measure impact, not activity : Prioritize real user outcomes over just hitting deadlines. Align the whole team : Ensure every function shares the same goals and roadmap clarity."),
(19, 3, 2, 1,    NULL, 3, 0, 100,  70, 100, 1, "Fix what frustrates users : Focus on real pain points, not 'cool' ideas. Bet mostly on what's proven : Spend 70% on sure wins, 30% on bold bets. Only build what matters : Ship features that drive value, virality, or stickiness. Measure impact, not activity : Prioritize real user outcomes over just hitting deadlines. Align the whole team : Ensure every function shares the same goals and roadmap clarity."),
(20, 3, 2, 2,    NULL, 3, 0, 100,  60, 100, 1, "Fix what frustrates users : Focus on real pain points, not 'cool' ideas. Bet mostly on what's proven : Spend 70% on sure wins, 30% on bold bets. Only build what matters : Ship features that drive value, virality, or stickiness. Measure impact, not activity : Prioritize real user outcomes over just hitting deadlines. Align the whole team : Ensure every function shares the same goals and roadmap clarity."),
(21, 4, 2, 1,    NULL, 3, 0, 100,  85, 100, 1, "Fix what frustrates users : Focus on real pain points, not 'cool' ideas. Bet mostly on what's proven : Spend 70% on sure wins, 30% on bold bets. Only build what matters : Ship features that drive value, virality, or stickiness. Measure impact, not activity : Prioritize real user outcomes over just hitting deadlines. Align the whole team : Ensure every function shares the same goals and roadmap clarity."),
(22, 4, 2, 2,    NULL, 3, 0, 100,  75, 100, 1, "Fix what frustrates users : Focus on real pain points, not 'cool' ideas. Bet mostly on what's proven : Spend 70% on sure wins, 30% on bold bets. Only build what matters : Ship features that drive value, virality, or stickiness. Measure impact, not activity : Prioritize real user outcomes over just hitting deadlines. Align the whole team : Ensure every function shares the same goals and roadmap clarity."),
(23, 5, 2, 1,    NULL, 3, 0, 100,  90, 100, 1, "Fix what frustrates users : Focus on real pain points, not 'cool' ideas. Bet mostly on what's proven : Spend 70% on sure wins, 30% on bold bets. Only build what matters : Ship features that drive value, virality, or stickiness. Measure impact, not activity : Prioritize real user outcomes over just hitting deadlines. Align the whole team : Ensure every function shares the same goals and roadmap clarity."),
(24, 5, 2, 2,    NULL, 3, 0, 100,  80, 100, 1, "Fix what frustrates users : Focus on real pain points, not 'cool' ideas. Bet mostly on what's proven : Spend 70% on sure wins, 30% on bold bets. Only build what matters : Ship features that drive value, virality, or stickiness. Measure impact, not activity : Prioritize real user outcomes over just hitting deadlines. Align the whole team : Ensure every function shares the same goals and roadmap clarity.");