Feature: Generate Recommendations
    Tests related to generating recommendations for specified metrics
# Metric recommendations can only be generated if the metric exists for that specific report, which is primarily
# determined by the growth stage of the company. The following scenarios test the generation of recommendations
# Note: 54 metrics exist in 07_metrics.sql, however, only 43 unique metrics are stored in 
# 09_architecture_growth_stage_metrics.sql which is the source of metric generation for the report.
#|------------------------------------To test the 43 test cases below--------------------------------------|
#|--------------------------------------<pytest -m metric_rec_test>----------------------------------------|
#|---------------------------------------------------------------------------------------------------------|


    @growth_stage_2
    @metric_rec_test
    Scenario Outline: Using a specific report with Growth Stage 2, generate the correct recommendations
        Given the SaaS Type is "B2C"
        And the Company Orientation is "Horizontal"
        And the Industry is "All Industries"
        And the Annual Revenue is $"1.1" million
        And my company's "<metric>" metric is outside of the target range

        When I generate a report

        Then the report should display recommendations for "<metric>"
        Examples:
            | metric                                                 | metric_id |
            | % of Users 'Very Disappointed' if Product is Removed   | #5        |
            | Net Revenue Retention (NRR)                            | #9        |
            | Gross Margin                                           | #14       |
            | Net Burn Rate                                          | #23       |
            | Burn Multiple                                          | #24       |
            | Percentage of Roadmap Influenced by Data               | #31       |
            | The Ratio of GTM Spend to New ARR                      | #32       |
            | Percentage Strategic Founder Time                      | #46       |
            | Percentage Operational Founder Time                    | #47       |
            | Competitive Win Rate                                   | #53       |
              

    @growth_stage_3
    @metric_rec_test
    Scenario Outline: Using a specific report with Growth Stage 3, generate the correct recommendations
        Given the SaaS Type is "All SaaS Types"
        And the Company Orientation is "Horizontal"
        And the Industry is "All Industries"
        And the Annual Revenue is $"2.1" million
        And my company's "<metric>" metric is outside of the target range

        When I generate a report

        Then the report should display recommendations for "<metric>"
        Examples:
            | metric                                                            | metric_id |
            | Average Release Cycle Time                                        | #4        |
            | Monthly Churn Rate                                                | #8        |
            | LTV:CAC Ratio                                                     | #15       |
            | ARR Growth Rate                                                   | #19       |
            | Annual Recurring Revenue (ARR) per Employee or Revenue Efficiency | #25       |
            | Percentage of Engineering Time on Rework                          | #35       |
            | Funnel Analytics Completeness                                     | #37       |
            | Percentage Revenue From Non-founder Deals                         | #40       |
            | Lead Conversion Rate from MQL to SQL                              | #50       |
            | Span of Control                                                   | #54       |
        
    @growth_stage_4
    @metric_rec_test
    Scenario Outline: Using a specific report with Growth Stage 4, generate the correct recommendations
        Given the SaaS Type is "All SaaS Types"
        And the Company Orientation is "Horizontal"
        And the Industry is "All Industries"
        And the Annual Revenue is $"4.1" million
        And my company's "<metric>" metric is outside of the target range

        When I generate a report

        Then the report should display recommendations for "<metric>"
        Examples:
            | metric                                       | metric_id |
            | % of Features Used by >50% of Users          | #6        |
            | Customer Retention Rate (CRR)                | #7        |
            | ARR Growth Rate                              | #19       |
            | Percentage of KPIs with Real-Time Visibility | #36       |
            | Average Time to Close Tickets (ops/dev)      | #38       |
            | Uptime                                       | #41       |
            | Latency                                      | #42       |
            | Decision Cycle Time (DCT)                    | #49       |
            | % of Roles with OKRs                         | #52       |
            
    @growth_stage_5
    @metric_rec_test
    Scenario Outline: Using a specific report with Growth Stage 5, generate the correct recommendations
        Given the SaaS Type is "B2C"
        And the Company Orientation is "Horizontal"
        And the Industry is "All Industries"
        And the Annual Revenue is $"7.1" million
        And my company's "<metric>" metric is outside of the target range

        When I generate a report

        Then the report should display recommendations for "<metric>"
        Examples:
            | metric                                                                      | metric_id |
            | Net Promoter Score                                                          | #1        |
            | Customer Satisfaction Score (CSAT)                                          | #2        |
            | % of Roadmap Delivered Quarterly                                            | #3        |
            | % Revenue from Upsell                                                       | #21       |
            | % Revenue from Cross-sell                                                   | #22       |
            | Earnings Before Interest, Taxes, Depreciation & Amortization (EBITDA) Margin| #27       |
            | Compound Annual Growth Rate (CAGR)                                          | #28       | 
            | The Rule Of 40                                                              | #29       | 
            | Cost of Goods Sold COGS as a Percentage Of Revenue                          | #33       | 
            | Data Coverage Ratio                                                         | #43       | 
            | User Adoption Rate                                                          | #44       | 
            | Decision Consistency Score                                                  | #45       | 
            | Percentage of Team Aligned on Top Three Priorities                          | #48       | 
            | Team Engagement Score                                                       | #51       | 