import pytest
from unittest import mock
from tests.fixtures.report_page_data import *
from src.components.report import format_value_with_unit
from src.db_queries.metrics import get_metrics
from src.components.metrics import get_slider_format
from src.db_queries.recommendations import get_recommendations

DEBUG_ENABLED = False


def report_generator(saas_type_id, orientation, industry_id, annual_revenue_million, gen_recommendations):
    """Test report generation app with complete session state
    Args
        saas_type_id (int) : Can be 0, 1, or 2. 0 --> All SaaS, 1 --> B2C, 2 --> B2B2C
        orientation (str) : Can be Horizontal or Vertical
        industry_id (int) : Can be an integer in [1, 10] or 99
        annual_revenue_million (float) : Annual revenue in millions. 
        gen_recommendations (bool) : True to manipulate "user-input" outside of target values to trigger recommendation generation
    """
    #Set up Streamlit AppTest
    app = AppTest.from_file("../../report_page.py")  # Get the AppTest instance
    generate_metrics(saas_type_id, orientation, industry_id, annual_revenue_million, app , gen_recommendations)
    app.run()  # Run the app
    
    #For other verification purposes in other tests that utilize this report generator test
    

    check_report_results(app, gen_recommendations)
    


def check_report_results(app, gen_recommendations):
    results = {'num_of_metrics' : 0, 'generated_recommendations' : []}
    # Verify that the report generation logic is called
    assert app.title[0].value == "🧬 SaaS Traction Diagnostic Report"
    assert app.markdown[len(app.markdown)-1].value == """1. **Prioritize 3 Key Actions** from recommendations\n2. **Establish Baseline Metrics** within 7 days\n3. **Create 30/60/90 Day Plan** with milestones"""
    assert app.error == [], "Errors in report generation were found"  # Ensure no errors were raised during report generation
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
            #Check that the user input values are correct
            assert row[1] == format_value_with_unit(
                app.session_state['metric_' + str(i+1) + '_' + str(app.session_state['metrics_cache'][row[0]]['metric_id'])], 
                app.session_state['metrics_cache'][row[0]]['unit'])
            #Check that the recommended ranges are correct
            assert row[2] == str(app.session_state['metrics_cache'][row[0]]['target_low_range']) + ' - ' + \
                str(app.session_state['metrics_cache'][row[0]]['target_high_range']) + ' ' + \
                app.session_state['metrics_cache'][row[0]]['unit']
            results['num_of_metrics'] += 1
            
    #Check for recommendations if toggled
    if (gen_recommendations):
        assert len(app.metric) > 4, "There should be more than 4 metrics element if recommendations are generated."
        rec_db = get_recommendations()
        #Only recommendations uses containers in the report generation
        for expander in app.expander:
            column_count = 0
            metric_id = None
            metric_name = ""
            for column in expander.columns:
                #Because of the fact that "container" elements cannot be referenced
                #The best we can do for now is to source the columns from the expander subdivisions
                #We still need to filter out some what seems like place holder columns that distinctly have weights of 0.5
                if column.weight != 0.5:
                    #Columns come in pairs
                    if column_count % 2 == 0:
                        #This gives us the metric
                        #It would probably be easier if the elements were uniquely tagged
                        #However, making work with what we have this can identify the metric for us
                        subheader = column.subheader.values[0]
                        metric_name = str.removeprefix(subheader, '🚨 ')
                        metric_id = app.session_state['metrics_cache'][metric_name]['metric_id']
                        debug_print(f"Metric ID: {metric_id}, Metric Name: {metric_name}")
                    elif metric_id:
                        if (metric_id > len(rec_db)):
                            assert column.info[0].value == "No specific recommendations available. Review general best practices."
                        else:
                            #This gives us the recommendations
                            #At this point, we can gurantee recommendations exist, meaning markdown "Recommended Actions" needed to be removed
                            rec_mark_down_list = column.markdown[1:] #Trim off the first index for "Recommended Actions"
                            #If the extra resource markdown exists, trim that off too
                            if (rec_mark_down_list[-1].value == "#### 📚 Resources"):
                                rec_mark_down_list = rec_mark_down_list[:-1]

                            
                            metric_rec_list = rec_db[metric_id]
                            assert len(metric_rec_list) == len(rec_mark_down_list)
                            for metric_rec, mark_rec in zip(metric_rec_list, rec_mark_down_list):
                                assert metric_rec in mark_rec.value
                            results['generated_recommendations'].append(metric_name)
                    column_count +=1
    #If no recommendations, then only 4 metric elements should exist
    else:
        assert len(app.metric) == 4, "There should be only 4 metric elements if no recommendations are generated."
    
    return results

#----------------------helper functions----------------------

# Debug print function that can be toggled on or off
# This is useful for debugging without cluttering the test output
def debug_print(*args):
    """Debug print function to avoid cluttering test output"""
    if DEBUG_ENABLED:
        print(*args)

def generate_metrics(saas_type_id, orientation, industry_id, annual_revenue_million, app , gen_recommendations = False):
    """
    Generates metric data to store into app.session_state['metric_cache']

    Args
        saas_type_id (int) : Can be 0, 1, or 2. 0 --> All SaaS, 1 --> B2C, 2 --> B2B2C.
        orientation (string) : Can be 'Horizontal' or 'Vertical'.
        industry_id (int) : Can be an integer in [1, 10] or 99.
        annual_revenue_million (float) : Annual revenue in millions. 
        app (Obj AppTest) : AppTest object to store data into. 
        gen_recommendations (bool) : True to manipulate "user-input" outside of target values to trigger recommendation generation. Defaults to False.

    """
    #Load in all required keys to session state
    for key, value in mock_default_session_state.items():
        app.session_state[key] = value
    #Override session state with modified values
    app.session_state['selected_saas_type'] = mock_saas_types[saas_type_id]['type_name']
    app.session_state['selected_orientation'] = orientation
    app.session_state['selected_industry'] = mock_industries[industry_id]['industry_name']
    app.session_state['annual_revenue'] = annual_revenue_million
    growth_stage = calculate_growth_stage_index(annual_revenue_million)
    app.session_state['growth_stage_id'] = growth_stage
    app.session_state['growth_stage_name'] = mock_growth_stages_max_revenue[growth_stage - 1]['growth_stage_name']
    app.session_state['metrics_cache'].clear()
    for pillar_id in range(1, 5):
        #Based on src.components.metrics.py::display_metrics_for_pillars
        metrics_dict = get_metrics(
            growth_stage_id= growth_stage,
            architecture_pillar_id= pillar_id,
            saas_type_id= saas_type_id,
            industry_id= industry_id
            )
        for metric_id, metric in metrics_dict.items():
            metric_info = {
                        "persistent_key": f"metric_{pillar_id}_{metric_id}",
                        "pillar_id": pillar_id,
                        "pillar_name": mock_pillar_names[pillar_id-1], #Pillar_id is off by 1 since pillar_names starts at 0, not 1
                        "metric_id": metric_id,
                        "unit": metric['units'],
                        "target_low_range": float(metric['lo_range_value']),
                        "target_high_range": float(metric['hi_range_value']),
                        "slider_format": get_slider_format(metric['units']),
                        "blog_link": metric['blog_link'],
                        "video_link": metric['video_link'],
                    }
            app.session_state['metrics_cache'][metric['metric_name']] = metric_info
            #Generate user input data
            if (gen_recommendations):
                #Trigger recommendations by setting uesr input outside of target range
                app.session_state[f"metric_{pillar_id}_{metric_id}"] = 1 + metric['hi_range_value']
            else:
                app.session_state[f"metric_{pillar_id}_{metric_id}"] = float(metric['lo_range_value'] + metric['hi_range_value']) / 2
    debug_print(app.session_state)

def calculate_growth_stage_index(annual_revenue):
    stage_idx = 1
    for max_rev in mock_growth_stages_max_revenue:
        if annual_revenue > max_rev['growth_stage_max']:
            stage_idx += 1
        else:
            return stage_idx
    debug_print("Annual Revenue too high: " + annual_revenue + " million.")
    return -1


def clear_session_state(app):
    """
    Clears the session state AFTER a test is completed
    """
    for metric in app.session_state['metrics_cache']:
        del app.session_state[metric['persistent_key']]
    for key in mock_default_session_state:
        del app.session_state[key]