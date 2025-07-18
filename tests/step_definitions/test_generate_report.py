import pytest  
from streamlit.testing.v1 import AppTest
from pytest_bdd import scenarios, scenario, given, when, then, parsers
from tests.integration_tests.report_page_integration import report_generator, check_report_results, generate_metrics
from tests.fixtures.report_page_data import mock_saas_types, mock_industries
# Load all scenarios from the feature file  
scenarios("../features/generate_report.feature")  
scenarios("../features/generate_recommendations.feature")
# Fixtures  
@pytest.fixture  
def session_state():  
    return {'selected_saas_type' : "All SaaS Types",
            'selected_orientation' : "Vertical",
            'selected_industry' : "All Industries",
            'annual_revenue': 0,
            'report_results' : {},
            'gen_recs_for' : [] }  # Using a dictionary to allow modifications  
  
# Given Steps  
@given(parsers.parse('the SaaS Type is "{saas_type}"'))  
def initial_saas_type(saas_type, session_state):  
    #Identify saas_index off of type name
    saas_id = -1
    for idx, type_name in mock_saas_types.items():
        if type_name['type_name'] == saas_type:
            saas_id = idx
            break
    assert saas_id != -1, f"Type '{saas_type}' not valid. Valid types are: 'All SaaS Types', 'B2C', or 'B2B2C'."
    session_state['selected_saas_type'] = saas_id

@given(parsers.parse('the Company Orientation is "{orientation}"'))
def initial_orientation(orientation, session_state):
    assert orientation == 'Vertical' or orientation == 'Horizontal', (
        f"Orientation '{orientation}' not valid. Valid orientations are: 'Horizontal' or 'Vertical'.")
    session_state['selected_orientation'] = orientation
    
@given(parsers.parse('the Industry is "{industry}"'))
def initial_industry(industry, session_state):
    ind_id = -1
    for idx, industry_name in mock_industries.items():
        if industry_name['industry_name'].strip().lower() == industry.strip().lower():
            ind_id = idx
            break
    assert ind_id != -1, (f"""
                          Type '{industry}' not valid. 
                          Valid types are: 'All Industries', 'Healthcare', 'Financial Services',
                          'Retail/E-commerce', 'Manufacturing', 'Construction',
                          'Logistics/Supply Chain', 'Insurance', 'Hospitality',
                          'Education', 'Real Estate', 'Other'
                          """)
    session_state['selected_industry'] = ind_id

@given(parsers.parse('the Annual Revenue is $"{revenue}" million'))
def initial_revenue(revenue, session_state):
    session_state['annual_revenue'] = float(revenue)

@given(parsers.parse('my company\'s "{metric}" metric is outside of the target range'))
def modify_metric(metric, session_state):
    if metric not in session_state.get("gen_recs_for", []):
        session_state.get("gen_recs_for").append(metric)
    


# When Steps  
@when("I generate a report")  
def create_report(session_state):  
    app = AppTest.from_file("../../report_page.py")  # Get the AppTest instance
    generate_metrics(session_state['selected_saas_type'],
                    session_state['selected_orientation'],
                    session_state['selected_industry'],
                    session_state['annual_revenue'],
                    app,
                    False)
    
    recs_generated = False
    for metric in session_state['gen_recs_for']:
        metric_data = app.session_state['metrics_cache'].get(metric, None)
        assert metric_data != None, f"Metric '{metric}' was not found in the metrics_cache: {app.session_state['metrics_cache'].keys()}"
        app.session_state[metric_data['persistent_key']] = metric_data['target_high_range'] + 1
        recs_generated = True
    
    
    app.run()
    session_state['report_results'] = check_report_results(app, recs_generated)




# Then Steps  
@then(parsers.parse('the report should display "{num_of_metrics}" data metrics'))  
def metric_count_should_be(num_of_metrics, session_state):  
    error_message = f"The expected metric count {num_of_metrics} did not match " +\
                    f"the actual count of {session_state['report_results']['num_of_metrics']}."
    assert int(num_of_metrics) == session_state['report_results']['num_of_metrics'], error_message

@then(parsers.parse('the report should display recommendations for "{rec}"'))
def recommendation_count_should_be(rec, session_state):
    error_message = f"The expected metric {rec} did not appear " +\
        f"in the list of generated recommendations: {session_state['report_results']['generated_recommendations']}."
    
    assert rec in session_state['report_results']['generated_recommendations'], error_message
