Feature: Generate Report
    Tests related to report generation

# This feature file tests the generation of reports based on different parameters 
# such as SaaS Type, Company Orientation, Industry, and Annual Revenue.
# I've also realized that the report generation is NOT dependent on orientaion whatsoever.
# If wanted, orientation permutations can be removed from the tests and have been commented out
# and moved to the bottom for easy removal. This reduces test cases from the original 72 -> 36
# However, for the time being, they will be kept in case they are needed in the future.

    @unit
    Scenario: Generate Report
    
        Given the SaaS Type is "All SaaS Types"
        And the Company Orientation is "Horizontal"
        And the Industry is "All Industries"
        And the Annual Revenue is $"1.5" million
        And my company's "Gross Margin" metric is outside of the target range
        And my company's "Net Burn Rate" metric is outside of the target range

        When I generate a report
        
        Then the report should display "10" data metrics
        And the report should display recommendations for "Gross Margin"
        And the report should display recommendations for "Net Burn Rate"

#Below are the test sets based on this @unit test. They do NOT check for metrics/recommendations.
#This is also similarly based on the Integration Test parameters in tests/integration_tests/test_report_page_integration.py
#To run ALL these 72 total tests: pytest -m "all_industries or retail or manufacturing"
#Each test takes on average 3 seconds. Keep that in mind with large scale testing.
#Smaller scale test promps are provided at "check points" below in segments
#Test breakdown structure:
#Industries (3)
#   |-----Orientation (1) (Removed "Vertical" as it does not change the report)
#               |-------SaaS Type (3)


#|------------------------------------To test the 24 test cases below--------------------------------------|
#|---------------------------<Check Point (24 Tests): pytest -m all_industries>----------------------------|
#|---------------------------------------------------------------------------------------------------------|
#||----------------------------------To Test the 12 test cases below:-------------------------------------||
#||-------------<Check Point (12 Tests): pytest -m "horizontal and all_industries">-----------------------||
#||-------------------------------------------------------------------------------------------------------||

    @all_saas
    @horizontal
    @all_industries
    Scenario Outline: Generate with All SaaS Types, Horizontal orientation, and All Industries
        Given the SaaS Type is "<saas_type>"
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type      | orientation | industry       | revenue | metric_count |
            | All SaaS Types | Horizontal  | All Industries | 1.1     | 10           |
            | All SaaS Types | Horizontal  | All Industries | 2.1     | 11           |
            | All SaaS Types | Horizontal  | All Industries | 4.1     | 12           |
            | All SaaS Types | Horizontal  | All Industries | 7.1     | 12           |
    
    @B2C
    @horizontal
    @all_industries
    Scenario Outline: Generate with B2C SaaS Type, Horizontal orientation, and All Industries
        Given the SaaS Type is "<saas_type>"
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type | orientation | industry       | revenue | metric_count |
            | B2C       | Horizontal  | All Industries | 1.1     | 12           |
            | B2C       | Horizontal  | All Industries | 2.1     | 11           |
            | B2C       | Horizontal  | All Industries | 4.1     | 12           |
            | B2C       | Horizontal  | All Industries | 7.1     | 14           |
    
    @B2B2C
    @horizontal
    @all_industries
    Scenario Outline: Generate with B2B2C SaaS Type, Horizontal orientation, and All Industries
        Given the SaaS Type is "<saas_type>" 
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type | orientation | industry       | revenue | metric_count |
            | B2B2C     | Horizontal  | All Industries | 1.1     | 12           |
            | B2B2C     | Horizontal  | All Industries | 2.1     | 11           |
            | B2B2C     | Horizontal  | All Industries | 4.1     | 15           |
            | B2B2C     | Horizontal  | All Industries | 7.1     | 13           |

#|------------------------------------To test the 24 test cases below--------------------------------------|
#|------------------------------<Check Point (24 Tests): pytest -m retail>---------------------------------|
#|---------------------------------------------------------------------------------------------------------|
#||-----------------------------------To test the 12 test cases below-------------------------------------||
#||----------------------<Check Point (12 Tests): pytest -m "horizontal and retail">----------------------||
#||-------------------------------------------------------------------------------------------------------||
    @all_saas
    @horizontal
    @retail
    Scenario Outline: Generate with All SaaS Types, Horizontal orientation, and Retail/E-commerce
        Given the SaaS Type is "<saas_type>"
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type      | orientation | industry          | revenue | metric_count |
            | All SaaS Types | Horizontal  | Retail/E-commerce | 1.1     | 10           |
            | All SaaS Types | Horizontal  | Retail/E-commerce | 2.1     | 11           |
            | All SaaS Types | Horizontal  | Retail/E-commerce | 4.1     | 15           |
            | All SaaS Types | Horizontal  | Retail/E-commerce | 7.1     | 12           |
    
    @B2C
    @horizontal
    @retail
    Scenario Outline: Generate with B2C SaaS Type, Horizontal orientation, and Retail/E-commerce
        Given the SaaS Type is "<saas_type>"
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type | orientation | industry          | revenue | metric_count |
            | B2C       | Horizontal  | Retail/E-commerce | 1.1     | 12           |
            | B2C       | Horizontal  | Retail/E-commerce | 2.1     | 11           |
            | B2C       | Horizontal  | Retail/E-commerce | 4.1     | 15           |
            | B2C       | Horizontal  | Retail/E-commerce | 7.1     | 14           |
    
    @B2B2C 
    @horizontal
    @retail
    Scenario Outline: Generate with B2B2C SaaS Type, Horizontal orientation, and Retail/E-commerce
        Given the SaaS Type is "<saas_type>" 
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type | orientation | industry          | revenue | metric_count |
            | B2B2C     | Horizontal  | Retail/E-commerce | 1.1     | 12           |
            | B2B2C     | Horizontal  | Retail/E-commerce | 2.1     | 11           |
            | B2B2C     | Horizontal  | Retail/E-commerce | 4.1     | 15           |
            | B2B2C     | Horizontal  | Retail/E-commerce | 7.1     | 13           |

#|------------------------------------To test the 24 test cases below--------------------------------------|
#|---------------------------<Check Point (24 Tests): pytest -m manufacturing>-----------------------------|
#|---------------------------------------------------------------------------------------------------------|
#||-----------------------------------To test the 12 test cases below-------------------------------------||
#||-------------------<Check Point (12 Tests): pytest -m "horizontal and manufacturing">------------------||
#||-------------------------------------------------------------------------------------------------------||
    @all_saas
    @horizontal
    @manufacturing
    Scenario Outline: Generate with All SaaS Types, Horizontal orientation, and Manufacturing
        Given the SaaS Type is "<saas_type>"
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type      | orientation | industry          | revenue | metric_count |
            | All SaaS Types | Horizontal  | Manufacturing     | 1.1     | 10           |
            | All SaaS Types | Horizontal  | Manufacturing     | 2.1     | 11           |
            | All SaaS Types | Horizontal  | Manufacturing     | 4.1     | 15           |
            | All SaaS Types | Horizontal  | Manufacturing     | 7.1     | 12           |
    
    @B2C
    @horizontal
    @manufacturing
    Scenario Outline: Generate with B2C SaaS Type, Horizontal orientation, and Manufacturing
        Given the SaaS Type is "<saas_type>"
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type | orientation | industry      | revenue | metric_count |
            | B2C       | Horizontal  | Manufacturing | 1.1     | 12           |
            | B2C       | Horizontal  | Manufacturing | 2.1     | 11           |
            | B2C       | Horizontal  | Manufacturing | 4.1     | 15           |
            | B2C       | Horizontal  | Manufacturing | 7.1     | 14           |
    
    @B2B2C 
    @horizontal
    @manufacturing
    Scenario Outline: Generate with B2B2C SaaS Type, Horizontal orientation, and Manufacturing
        Given the SaaS Type is "<saas_type>" 
        And the Company Orientation is "<orientation>"
        And the Industry is "<industry>"
        And the Annual Revenue is $"<revenue>" million

        When I generate a report

        Then the report should display "<metric_count>" data metrics

        Examples:
            | saas_type | orientation | industry      | revenue | metric_count |
            | B2B2C     | Horizontal  | Manufacturing | 1.1     | 12           |
            | B2B2C     | Horizontal  | Manufacturing | 2.1     | 11           |
            | B2B2C     | Horizontal  | Manufacturing | 4.1     | 15           |
            | B2B2C     | Horizontal  | Manufacturing | 7.1     | 13           |






# #||-------------------------------------------------------------------------------------------------------||
# #||--------------<Check Point (12 Tests): pytest -m "vertical and all_industries">------------------------||
# #||-------------------------------------------------------------------------------------------------------||
    #     @all_saas
    #     @vertical
    #     @all_industries
    #     Scenario Outline: Generate with All SaaS Type, Vertical orientation, and All Industries
    #         Given the SaaS Type is "<saas_type>"
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type      | orientation | industry       | revenue | metric_count |
    #             | All SaaS Types | Vertical    | All Industries | 1.1     | 10           |
    #             | All SaaS Types | Vertical    | All Industries | 2.1     | 11           |
    #             | All SaaS Types | Vertical    | All Industries | 4.1     | 12           |
    #             | All SaaS Types | Vertical    | All Industries | 7.1     | 12           |
        
    #     @B2C
    #     @vertical
    #     @all_industries
    #     Scenario Outline: Generate with B2C SaaS Type, Vertical orientation, and All Industries
    #         Given the SaaS Type is "<saas_type>"
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type | orientation | industry       | revenue | metric_count |
    #             | B2C       | Vertical    | All Industries | 1.1     | 12           |
    #             | B2C       | Vertical    | All Industries | 2.1     | 11           |
    #             | B2C       | Vertical    | All Industries | 4.1     | 12           |
    #             | B2C       | Vertical    | All Industries | 7.1     | 14           |
        
    #     @B2B2C
    #     @vertical
    #     @all_industries
    #     Scenario Outline: Generate with B2B2C SaaS Type, Vertical orientation, and All Industries
    #         Given the SaaS Type is "<saas_type>" 
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type | orientation | industry       | revenue | metric_count |
    #             | B2B2C     | Vertical    | All Industries | 1.1     | 12           |
    #             | B2B2C     | Vertical    | All Industries | 2.1     | 11           |
    #             | B2B2C     | Vertical    | All Industries | 4.1     | 15           |
    #             | B2B2C     | Vertical    | All Industries | 7.1     | 13           |
# #||-----------------------------------To test the 12 test cases below-------------------------------------||
# #||----------------------<Check Point (12 Tests): pytest -m "vertical and retail">------------------------||
# #||-------------------------------------------------------------------------------------------------------||
    #     @all
    #     @vertical
    #     @retail
    #     Scenario Outline: Generate with All SaaS Type, Vertical orientation, and Retail/E-commerce
    #         Given the SaaS Type is "<saas_type>"
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type      | orientation | industry          | revenue | metric_count |
    #             | All SaaS Types | Vertical    | Retail/E-commerce | 1.1     | 10           |
    #             | All SaaS Types | Vertical    | Retail/E-commerce | 2.1     | 11           |
    #             | All SaaS Types | Vertical    | Retail/E-commerce | 4.1     | 15           |
    #             | All SaaS Types | Vertical    | Retail/E-commerce | 7.1     | 12           |

    #     @B2C
    #     @vertical
    #     @retail
    #     Scenario Outline: Generate with B2C SaaS Type, Vertical orientation, and Retail/E-commerce
    #         Given the SaaS Type is "<saas_type>"
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type | orientation | industry          | revenue | metric_count |
    #             | B2C       | Vertical    | Retail/E-commerce | 1.1     | 12           |
    #             | B2C       | Vertical    | Retail/E-commerce | 2.1     | 11           |
    #             | B2C       | Vertical    | Retail/E-commerce | 4.1     | 15           |
    #             | B2C       | Vertical    | Retail/E-commerce | 7.1     | 14           |

    #     @B2B2C
    #     @vertical
    #     @retail
    #     Scenario Outline: Generate with B2B2C SaaS Type, Vertical orientation, and Retail/E-commerce
    #         Given the SaaS Type is "<saas_type>" 
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type | orientation | industry          | revenue | metric_count |
    #             | B2B2C     | Vertical    | Retail/E-commerce | 1.1     | 12           |
    #             | B2B2C     | Vertical    | Retail/E-commerce | 2.1     | 11           |
    #             | B2B2C     | Vertical    | Retail/E-commerce | 4.1     | 15           |
    #             | B2B2C     | Vertical    | Retail/E-commerce | 7.1     | 13           |
# #||-----------------------------------To test the 12 test cases below-------------------------------------||
# #||--------------------<Check Point (12 Tests): pytest -m "vertical and manufacturing">-------------------||
# #||-------------------------------------------------------------------------------------------------------||
    #     @all
    #     @vertical
    #     @manufacturing
    #     Scenario Outline: Generate with All SaaS Type, Vertical orientation, and Manufacturing
    #         Given the SaaS Type is "<saas_type>"
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type      | orientation | industry      | revenue | metric_count |
    #             | All SaaS Types | Vertical    | Manufacturing | 1.1     | 10           |
    #             | All SaaS Types | Vertical    | Manufacturing | 2.1     | 11           |
    #             | All SaaS Types | Vertical    | Manufacturing | 4.1     | 15           |
    #             | All SaaS Types | Vertical    | Manufacturing | 7.1     | 12           |
        
    #     @B2C
    #     @vertical
    #     @manufacturing
    #     Scenario Outline: Generate with B2C SaaS Type, Vertical orientation, and Manufacturing
    #         Given the SaaS Type is "<saas_type>"
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type | orientation | industry      | revenue | metric_count |
    #             | B2C       | Vertical    | Manufacturing | 1.1     | 12           |
    #             | B2C       | Vertical    | Manufacturing | 2.1     | 11           |
    #             | B2C       | Vertical    | Manufacturing | 4.1     | 15           |
    #             | B2C       | Vertical    | Manufacturing | 7.1     | 14           |
        
    #     @B2B2C
    #     @vertical
    #     @manufacturing
    #     Scenario Outline: Generate with B2B2C SaaS Type, Vertical orientation, and Manufacturing
    #         Given the SaaS Type is "<saas_type>" 
    #         And the Company Orientation is "<orientation>"
    #         And the Industry is "<industry>"
    #         And the Annual Revenue is $"<revenue>" million

    #         When I generate a report

    #         Then the report should display "<metric_count>" data metrics

    #         Examples:
    #             | saas_type | orientation | industry      | revenue | metric_count |
    #             | B2B2C     | Vertical    | Manufacturing | 1.1     | 12           |
    #             | B2B2C     | Vertical    | Manufacturing | 2.1     | 11           |
    #             | B2B2C     | Vertical    | Manufacturing | 4.1     | 15           |
    #             | B2B2C     | Vertical    | Manufacturing | 7.1     | 13           |