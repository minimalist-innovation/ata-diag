import logging
from decimal import Decimal

import streamlit as st

from src.db_queries.architecture_pillars import get_architecture_pillars
from src.db_queries.metrics import get_metrics

logger = logging.getLogger(__name__)


def get_step_size_for_slider(units):
    """Determine the appropriate step size based on the metric units"""
    if "Months" in units:
        return 1.0
    elif "Days" in units:
        return 5.0
    elif "Hours" in units:
        return 1.0
    elif "Milliseconds" in units:
        return 100.00
    elif "Currency" in units:
        return 1000.00
    elif "Percentage" in units:
        return 0.3
    else:
        return 0.5


def get_slider_format(units):
    """Determine the appropriate slider format based on the metric units"""
    if "Months" in units:
        return "%d"
    elif "Days" in units:
        return "%d days"
    elif "Hours" in units:
        return "%d hours"
    elif "Milliseconds" in units:
        return "%d ms"
    elif "Currency" in units:
        return "$%.2f"
    elif "Percentage" in units:
        return "%.1f%%"
    else:
        return "%.2f"


def create_slider(metric, pillar_name, step_size, default_value, slider_format):
    slider_key = f"slider_{pillar_name}_{metric['id']}"

    return st.slider(
        label=f"{metric['metric_name']} ({metric['units']})",
        min_value=Decimal(float(metric['min_value'])),
        max_value=Decimal(float(metric['max_value'])),
        value=Decimal(float(st.session_state.get(slider_key, default_value))),
        step=Decimal(float(step_size)),
        format=slider_format,
        key=slider_key
    )


def update_metric(key):
    st.session_state[key] = st.session_state[f"widget_{key}"]


def display_metrics_for_pillar(architecture_pillar_id, growth_stage_id, saas_type_id=None, industry_id=None):
    # Get metrics dictionary with ID keys
    metrics_dict = get_metrics(
        growth_stage_id=growth_stage_id,
        architecture_pillar_id=architecture_pillar_id,
        saas_type_id=saas_type_id,
        industry_id=industry_id
    )

    if not metrics_dict:
        st.write(f"No metrics found for this combination.")
        return

    # Get pillar name for display purposes
    pillar_name = (get_architecture_pillars()
                   .get(architecture_pillar_id, {})
                   .get('pillar_name',
                        f"Pillar {architecture_pillar_id}"))

    # Display each metric using dictionary values
    for metric_id, metric in metrics_dict.items():

        # Create a container for the metric with border
        with st.container(border=True):
            # Metric header
            st.markdown(f"## {metric['metric_name']}")

            # Create two columns for each metric
            desc_col, slider_col = st.columns([0.55, 0.45])

            with desc_col:
                # Description with read more
                if metric['blog_link']:
                    st.markdown(f"{metric['description']} _[Learn more]({metric['blog_link']}).._")
                else:
                    st.markdown(metric['description'])

                # Video hover functionality
                if metric['video_link']:
                    video_url = metric['video_link'].replace('watch?v=', 'embed/')
                    with st.popover("📹 Video Guide", help=f"Watch a short video about {metric['metric_name']}"):
                        st.video(video_url)

            with slider_col:
                # Add slight top padding for better alignment with description
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

                # Target range for slider
                # Add null check before float conversion
                target_low = float(metric.get('lo_range_value', 0.0))
                target_high = float(metric.get('hi_range_value', target_low + 100.0))  # Default 100-unit range
                target_range = f"**_{target_low}-{target_high} {metric['units']}_**"
                default_value = (target_low + target_high) / 2

                persistent_key = f"metric_{architecture_pillar_id}_{metric_id}"
                if persistent_key not in st.session_state:
                    st.session_state[persistent_key] = default_value

                # Slider configuration
                slider_format = get_slider_format(metric['units'])
                min_val = float(metric['min_value'])
                max_val = float(metric['max_value'])
                step_size = get_step_size_for_slider(metric['units'])

                st.slider(
                    label=f"The target range is [{target_range}]. What is your value:",
                    key=f"widget_{persistent_key}",
                    min_value=min_val,
                    max_value=max_val,
                    value=st.session_state[persistent_key],
                    step=step_size,
                    format=slider_format,
                    on_change=lambda k=persistent_key: update_metric(k)
                )

                # Store metrics info in the session_state
                metric_info = {
                    "persistent_key": persistent_key,
                    "pillar_id": architecture_pillar_id,
                    "pillar_name": pillar_name,
                    "metric_id": metric_id,
                    "unit": metric['units'],
                    "target_low_range": float(metric['lo_range_value']),
                    "target_high_range": float(metric['hi_range_value']),
                    "slider_format": slider_format,
                    "blog_link": metric['blog_link'],
                    "video_link": metric['video_link'],
                }
                # Store the target range separately in session_state
                st.session_state['metrics_cache'][metric['metric_name']] = metric_info

        # Add space between metrics
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
