
import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def app_report():
    return AppTest.from_file("../../report_page.py") 

mock_empty_session_state = {}

mock_complete_session_state = {
    #Initialization Data
    'page_history': [],
    'current_page': 'report_page.py',
    'selected_saas_type': 'All SaaS Types',
    'selected_orientation': 'Horizontal',
    'selected_industry': 'All Industries',
    'annual_revenue': 1250000,
    'growth_stage_id': 2,
    'growth_stage_name': 'Validation Seekers',
    'pillar_1_complete': True,
    'pillar_2_complete': True,
    'pillar_3_complete': True,

    #Metric Persistant Data
    # Pillar 1 Metric Data
    'metric_1_14': 65,
    'metric_1_23': 75000,
    'metric_1_24': 100,
    # Pillar 2 Metric Data
    'metric_2_5': 22.5,
    'metric_2_9': 25,
    # Pillar 3 Metric Data
    'metric_3_31': 35,
    'metric_3_46': 40,
    'metric_3_47': 60,
    # Pillar 4 Metric Data
    'metric_4_51': 65,
    'metric_4_53': 50,

    #Metric Cache Generation
    'metrics_cache': {
    # Pillar 1 Metrics
        'Gross Margin' : {
            'persistent_key' : 'metric_1_14',
            'pillar_id' : 1,
            'pillar_name' : 'Revenue',
            'metric_id' : 14,
            'unit' : 'Percentage',
            'target_low_range' : 50,
            'target_high_range' : 65,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        },
        'Net Burn Rate' : {
            'persistent_key' : 'metric_1_23',
            'pillar_id' : 1,
            'pillar_name' : 'Revenue',
            'metric_id' : 23,
            'unit' : 'Currency',
            'target_low_range' : 50000,
            'target_high_range' : 175000,
            'slider_format' : 'Currency',
            'blog_link' : "",
            "video_link": ""
        },
        'Burn Multiple' : {
            'persistent_key' : 'metric_1_24',
            'pillar_id' : 1,
            'pillar_name' : 'Revenue',
            'metric_id' : 24,
            'unit' : 'Percentage',
            'target_low_range' : 50,
            'target_high_range' : 200,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        },
    # Pillar 2 Metrics
        "% of Users 'Very Disappointed' if Product is Removed": {
            'persistent_key' : "metric_2_5",
            'pillar_id' : 2,
            'pillar_name' : 'Product',
            'metric_id' : 5,
            'unit' : 'Percentage',
            'target_low_range' : 15,
            'target_high_range' : 30,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        },
        "Net Revenue Retention (NRR)": {
            'persistent_key' : "metric_2_9",
            'pillar_id' : 2,
            'pillar_name' : 'Product',
            'metric_id' : "9",
            'unit' : 'Percentage',
            'target_low_range' : 20,
            'target_high_range' : 30,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        },
    # Pillar 3 Metrics
        "Percentage of Roadmap Influenced by Data": {
            'persistent_key' : "metric_3_31",
            'pillar_id' : 3,
            'pillar_name' : 'System',
            'metric_id' : "31",
            'unit' : 'Percentage',
            'target_low_range' : 30,
            'target_high_range' : 40,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        },
        "Percentage Strategic Founder Time": {
            'persistent_key' : "metric_3_46",
            'pillar_id' : 3,
            'pillar_name' : 'System',
            'metric_id' : "46",
            'unit' : 'Percentage',
            'target_low_range' : 35,
            'target_high_range' : 45,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        },
        "Percentage Operational Founder Time": {
            'persistent_key' : "metric_3_47",
            'pillar_id' : 3,
            'pillar_name' : 'System',
            'metric_id' : "47",
            'unit' : 'Percentage',
            'target_low_range' : 55,
            'target_high_range' : 65,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        },
    # Pillar 4 Metrics
        "Team Engagement Score": {
            'persistent_key' : "metric_4_51",
            'pillar_id' : 4,
            'pillar_name' : 'People',
            'metric_id' : "51",
            'unit' : 'Percentage',
            'target_low_range' : 60,
            'target_high_range' : 70,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        },
        "Competitive Win Rate": {
            'persistent_key' : "metric_4_53",
            'pillar_id' : 4,
            'pillar_name' : 'People',
            'metric_id' : "53",
            'unit' : 'Percentage',
            'target_low_range' : 45,
            'target_high_range' :55,
            'slider_format' : 'Percentage',
            'blog_link' : "",
            "video_link": ""
        }
    }
    
}



mock_error_messages = [
    "Complete company profile first",
    "❌ Complete all previous steps before generating report"
]

mock_cta_toasts = [
    {
        'message': "While your report is being generated, you can book a **FREE** strategy call to walk through your results and get a clear, **PERSONALIZED** plan.",
        'icon': "✨"
    },
    {
        'message': "Click the **✅ Expert Analysis of Your Metrics - Book Your FREE Call** button in the top toolbar.",
        'icon': "👆"
    },
    {
        'message': "30 minutes, no pressure - just clarity.",
        'icon': "👍"
    }
]

mock_unit_types = [
    "Percentage",
    "Currency",
    "Months",
    "Days",
    "Hours",
    "Milliseconds"
]
