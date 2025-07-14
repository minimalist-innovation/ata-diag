## Import necessary libraries and modules
import pytest
from unittest import mock
from tests.fixtures.report_page_data import *

# Import required modules and functions to test
from report_page import main
from src.components.cta_toast import show_sequential_cta_toasts
from src.components.report import format_value_with_unit
from src.db_queries.recommendations import get_recommendations, get_recommendations_for_metric
from src.db_queries.connection import get_db_connection

DEBUG_ENABLED = False  # Set to True to enable debug prints


#-------------------------------------------------------------
#---------------------report_page.py tests--------------------
#-------------------------------------------------------------


#Test case for main() function in report_page.py with no session state
@mock.patch("report_page.st")
def test_report_page_no_session_state(mock_st):
    """Test report page when session state is empty"""
    mock_st.session_state = mock_empty_session_state # Simulate no session state
    
    main() #Calls the main function of report_page
    
    #Expected outputs to call the two error messages
    #and redirect users to the company profile page
    mock_st.error.assert_has_calls([mock.call.write(mock_error_messages[0]), 
                                    mock.call.write(mock_error_messages[1])],any_order=True)
    mock_st.switch_page.assert_called_once_with("company_profile.py")


@mock.patch("src.components.report.generate_report", return_value=None)
@mock.patch("src.components.cta_toast.show_sequential_cta_toasts", return_value=None)
def test_report_page_complete_session_state(mock_show_cta_toasts, mock_generate_report):
    """Test report page with complete session state"""
    app = AppTest.from_file("../../report_page.py")  # Get the AppTest instance
    for key, value in mock_complete_session_state.items():
        app.session_state[key] = value  # Set the session state to complete stat
    app.run()  # Run the app
    assert app.error == []  # Ensure no errors were raised during report generation
    assert mock_show_cta_toasts.called
    assert mock_generate_report.called
    

    
    
# Checks that CTA_toats trigger properly when called
@mock.patch("src.components.cta_toast.st")
def test_show_sequential_cta_toasts(mock_st):
    """Test sequential CTA toasts display"""
    show_sequential_cta_toasts()
        
    # Verify that the toasts are displayed in order
    #Iterates through the mock_cta_toasts and checks if each toast was called with the correct message and icon
    for (i, toast) in enumerate(mock_cta_toasts):
        mock_st.toast.assert_any_call(toast['message'], icon=toast['icon'])
    
    assert mock_st.toast.call_count == len(mock_cta_toasts)  # Ensure all 3 toasts were called


#-------------------------------------------------------------
#--------------------report.py tests--------------------------
#-------------------------------------------------------------


#Checks that the format_value_with_unit function formats values correctly
@pytest.mark.parametrize("value, unit, expected_output", [
    #Check positive values
    (0.123456, "Percentage", "0.1%"),
    (1234.5678, "Currency", "$1234.57"),
    (30, "Months", "30 months"),
    (15, "Days", "15 days"),
    (2.5, "Hours", "2 hours"),
    (123.456, "Milliseconds", "123 ms"),
    #Check for zero values
    (0, "Percentage", "0.0%"),
    (0, "Currency", "$0.00"),
    (0, "Months", "0 months"),
    (0, "Days", "0 days"),
    (0, "Hours", "0 hours"),
    (0, "Milliseconds", "0 ms"),
    #check for negative values
    (-0.123456, "Percentage", "-0.1%"),
    (-1234.5678, "Currency", "$-1234.57"),
    (-30, "Months", "-30 months"),
    (-15, "Days", "-15 days"),
    (-2.5, "Hours", "-2 hours"),
    (-123.456, "Milliseconds", "-123 ms"),
    #Invalid Values (types)
    ("invalid_value", "Percentage", "invalid_value"), # Non-numeric value
    (None, "Percentage","None"), # None value
    ([], "Percentage",  "[]"), # Empty list
    ({}, "Percentage", "{}"),  # Empty dictionary
    ("123abc", "Percentage", "123abc"), # String with non-numeric characters
    #Invalid Units  
    (123.456, "Perc", "123.5"),
    (123.456, "Curr", "123.5"),
    (123.456, "Mont", "123.5"),
    (123.456, "Day", "123.5"),
    (123.456, "Hour", "123.5"),
    (123.456, "Mill", "123.5") 
]
)
def test_format_value_with_unit(value, unit, expected_output):
    """Test formatting function for values with units"""
    assert format_value_with_unit(value, unit) == expected_output
    
#Primarily checks for dataframe generation. Not recommendations (As that is conditional on user input)
#Recommendations are tested separately below and *correct* recommendation (metric element) generation will be in integration tests
@mock.patch("src.db_queries.recommendations.get_recommendations_for_metric", return_value=None)
def test_generate_report(mock_get_recommendations_for_metric):
    """Test report generation app with complete session state"""
    app = AppTest.from_string("""
    import streamlit as st
    from src.components.report import generate_report
    st.set_page_config(page_title="SaaS Traction Diagnostic Report")
    generate_report(st.session_state)  # Call the report generation function
    """)

    for key, value in mock_complete_session_state.items():
        app.session_state[key] = value  # Set the session state to complete stat
    # generate_report(app.session_state)  # Call the report generation function

    app.run()  # Run the app
    
    # Verify that the report generation logic is called
    assert app.title[0].value == "🧬 SaaS Traction Diagnostic Report"
    assert app.markdown[len(app.markdown)-1].value == """1. **Prioritize 3 Key Actions** from recommendations\n2. **Establish Baseline Metrics** within 7 days\n3. **Create 30/60/90 Day Plan** with milestones"""
    assert app.error == []  # Ensure no errors were raised during report generation
    for metric in app.metric:
        debug_print(metric.label, metric.value)  # Print each metric's label and value for debugging

    #There should be 4 dataframe metrics displayed in the report
    #1 for each of the 4 pillars: Revenue, Product, System, People
    assert len(app.dataframe) == 4
    #Check off Each Metric DataFrame Generated
    for i in range(len(app.dataframe)):
        df = app.dataframe[i].value.to_numpy()
        debug_print(df)
        for row in df:
            #Check that the user input values are correct/match the input data
            assert row[1] == format_value_with_unit(
                mock_complete_session_state['metric_' + str(i+1) + '_' + str(mock_complete_session_state['metrics_cache'][row[0]]['metric_id'])], 
                mock_complete_session_state['metrics_cache'][row[0]]['unit'])
            #Check that the recommended ranges are correct
            assert row[2] == str(mock_complete_session_state['metrics_cache'][row[0]]['target_low_range']) + ' - ' + \
                str(mock_complete_session_state['metrics_cache'][row[0]]['target_high_range']) + ' ' + \
                mock_complete_session_state['metrics_cache'][row[0]]['unit']


#-------------------------------------------------------------
#--------------------recommendations.py tests-----------------
#-------------------------------------------------------------


#Check recommendation generation for each metric
def test_get_recommendations_for_metric():
    """Test recommendation generation for each metric"""
    all_recommendations = get_recommendations()  # Get all recommendations
    assert len(all_recommendations) > 0  # Ensure there are some recommendations
    debug_print("All recommendations:", all_recommendations)
    # Test for a specific metric ID
    for metric_id in range(1,len(all_recommendations)):
        recommendations = get_recommendations_for_metric(metric_id)
        # Print the recommendations for debugging
        # debug_print("Recommendations for metric", metric_id, ":", recommendations)
        # Check that recommendations are returned
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0  # Ensure there are some recommendations
        assert recommendations == all_recommendations[metric_id]


#-------------------------------------------------------------
#--------------------connection.py tests----------------------
#-------------------------------------------------------------


@mock.patch("src.db_queries.connection.st")
def test_get_db_connection(mock_st):
    """Test database connection retrieval"""
    conn = get_db_connection()
    assert conn is not None  # Ensure the connection is not None
    assert mock_st.error.call_count == 0


#-------------------------------------------------------------
#-----------------------Helper Functions----------------------
#-------------------------------------------------------------


# Debug print function that can be toggled on or off
# This is useful for debugging without cluttering the test output
def debug_print(*args):
    """Debug print function to avoid cluttering test output"""
    if DEBUG_ENABLED:
        print(*args)
