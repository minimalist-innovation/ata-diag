import pytest
from streamlit.testing.v1 import AppTest
from unittest.mock import patch


# Mock return values for dropdown options
mock_saas_types = {
    1: {'type_name': 'B2C'},
    2: {'type_name': 'B2B2C'}
}

mock_orientations = {
    1: {'orientation_name': 'Horizontal'},
    2: {'orientation_name': 'VerticaL'}
}

mock_industries = {
    1: {'industry_name': 'Healthcare'},
    2: {'industry_name': 'Financial Services'},
    3: {'industry_name': 'Retail/E-commerce'},
    4: {'industry_name': 'Manufacturing'},
    5: {'industry_name': 'Construction'},
    6: {'industry_name': 'Logistics/Supply Chain'},
    7: {'industry_name': 'Insurance'},
    9: {'industry_name': 'Hospitality'},
    10: {'industry_name': 'Real Estate'},
    99: {'industry_name': 'Other'}
}


# Fixture for the AppTest instance
@pytest.fixture
def app():
    return AppTest.from_file("../company_profile.py") 


@patch("src.db_queries.saas_types.get_saas_types", return_value=mock_saas_types)
@patch("src.db_queries.orientations.get_orientations", return_value=mock_orientations)
@patch("src.db_queries.industries.get_all_industries", return_value=mock_industries)
@patch("src.db_queries.industries.get_industries", return_value=mock_industries)
def test_all_selectboxes(mock_get_inds, mock_get_all_inds, mock_orients, mock_saas, app):
    # Initialize required session keys 
    app.session_state["metrics_cache"] = {}
    app.session_state["page_history"] = []

    # Step 1: Run the initial app
    app.run()

    # Test SaaS type selectbox
    saas_select_box = app.selectbox(key="selected_saas_type_key")
    assert saas_select_box.label == "Select your SaaS company type:"
    saas_select_box.set_value(1)
    app.run()
    assert app.session_state['selected_saas_type'] == "B2C"

    # Test Orientations selectbox
    orientations_select_box = app.selectbox(key="selected_orientation_key")
    assert orientations_select_box.label ==  "Is your company Horizontal or Vertical SaaS?"
    orientations_select_box.set_value(1)
    app.run()
    assert app.session_state['selected_orientation'] == "Horizontal"
   
    # Test Industry selectbox
    industry_select_box = app.selectbox(key="selected_industry_key")
    industry_select_box.set_value(4)
    app.run()
    assert app.session_state['selected_industry'] == "Manufacturing"

