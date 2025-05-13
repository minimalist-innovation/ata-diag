import logging
from datetime import datetime
from decimal import Decimal

import pandas as pd
import streamlit as st

from src.db_queries.recommendations import get_recommendations_for_metric

logger = logging.getLogger(__name__)


# Report Generation Helpers
def get_progress_column_config(units):
    """Return a simple NumberColumn config based on units"""
    if "Percentage" in units:
        return st.column_config.NumberColumn(
            "Current Value",
            format="%.1f%%"
        )
    elif "Currency" in units:
        return st.column_config.NumberColumn(
            "Current Value",
            format="$%,.0f"
        )
    elif "Months" in units:
        return st.column_config.NumberColumn(
            "Current Value",
            format="%d months"
        )
    elif "Days" in units:
        return st.column_config.NumberColumn(
            "Current Value",
            format="%d days"
        )
    elif "Hours" in units:
        return st.column_config.NumberColumn(
            "Current Value",
            format="%d hours"
        )
    elif "Milliseconds" in units:
        return st.column_config.NumberColumn(
            "Current Value",
            format="%d ms"
        )
    else:
        return st.column_config.NumberColumn(
            "Current Value",
            format="%.1f"
        )


def format_value_with_unit(value, unit):
    """Format a value based on its unit type, similar to get_slider_format"""
    try:
        value = float(value)
        if "Percentage" in unit:
            return f"{value:.1f}%"
        elif "Currency" in unit:
            return f"${value:,.0f}"
        elif "Months" in unit:
            return f"{int(value)} months"
        elif "Days" in unit:
            return f"{int(value)} days"
        elif "Hours" in unit:
            return f"{int(value)} hours"
        elif "Milliseconds" in unit:
            return f"{int(value)} ms"
        else:
            return f"{value:.1f}"
    except (ValueError, TypeError):
        return str(value)


def generate_report(session_state):
    """Render report using Streamlit components"""
    try:
        # ----- Report Header -----
        st.title("🧬 SaaS Traction Diagnostic Report")
        st.markdown(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        st.markdown("---")

        # ----- Company Overview -----
        st.header("🏢 Company Profile")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Annual Revenue", f"${session_state['annual_revenue']}M")
            st.metric("Growth Stage", session_state['growth_stage_name'])
        with col2:
            st.metric("Business Model",
                      f"{session_state['selected_saas_type']} ({session_state['selected_orientation']})")
            st.metric("Industry", session_state['selected_industry'])
        st.markdown("---")

        # ----- Metrics Analysis -----
        st.header("📈 Metrics Diagnosis")

        # Group metrics by pillar
        pillars = {}
        for metric_name, metric_data in session_state['metrics_cache'].items():
            pillar_name = metric_data['pillar_name']
            pillars.setdefault(pillar_name, []).append(metric_name)

        # Display metrics by pillar
        for pillar_name, metric_names in pillars.items():
            with st.expander(f"### {pillar_name} Metrics", expanded=True):
                # Build and display metrics table
                metrics_data = []
                for metric_name in metric_names:
                    metric_data = session_state['metrics_cache'][metric_name]
                    persistent_key = f"metric_{metric_data['pillar_id']}_{metric_data['metric_id']}"

                    try:
                        # Attempt to get and convert the value to float
                        current_value = float(session_state.get(persistent_key, 0))
                    except (ValueError, TypeError):
                        # If conversion fails, use a default value
                        current_value = 0.0

                    metrics_data.append({
                        "Metric": metric_name,
                        "Current": Decimal(float(current_value)),
                        "Target": f"{metric_data['target_low_range']} - {metric_data['target_high_range']} {metric_data['unit']}"
                    })

                st.dataframe(
                    pd.DataFrame(metrics_data),
                    column_config={
                        "Metric": st.column_config.TextColumn(width="large"),
                        "Current": get_progress_column_config(metric_data['unit']),
                        "Target": "Target Range"
                    },
                    hide_index=True,
                    use_container_width=True
                )

                st.markdown("---")

                # Generate recommendations for each metric
                for metric_name in metric_names:
                    metric_data = session_state['metrics_cache'][metric_name]
                    persistent_key = f"metric_{metric_data['pillar_id']}_{metric_data['metric_id']}"
                    current_value = session_state.get(persistent_key, 0)

                    try:
                        current_value = float(current_value)
                        target_low = float(metric_data['target_low_range'])
                        target_high = float(metric_data['target_high_range'])
                    except (ValueError, TypeError) as e:
                        logger.error(f"Value conversion error for {metric_name}: {e}")
                        continue

                    # Only show recommendations for metrics outside target range
                    if current_value < target_low or current_value > target_high:
                        with st.container(border=True):
                            cols = st.columns([1, 3])

                            # Current vs Target
                            with cols[0]:
                                st.subheader(f"🚨 {metric_name}")
                                st.metric("Current",
                                          format_value_with_unit(current_value, metric_data['unit']))
                                st.metric("Target Range",
                                          f"{metric_data['target_low_range']}-{metric_data['target_high_range']}{metric_data['unit']}")

                            # Recommendations
                            with cols[1]:
                                recommendations = get_recommendations_for_metric(metric_data['metric_id'])
                                if recommendations:
                                    st.markdown("#### 🛠 Recommended Actions")
                                    for rec in recommendations:
                                        st.markdown(f"- {rec}")
                                else:
                                    st.info("No specific recommendations available. Review general best practices.")

                                # Resource links
                                if metric_data.get('blog_link') or metric_data.get('video_link'):
                                    st.markdown("#### 📚 Resources")
                                    res_cols = st.columns(2)
                                    if metric_data.get('blog_link'):
                                        res_cols[0].page_link(
                                            metric_data['blog_link'],
                                            label="Detailed Guide",
                                            icon="📖"
                                        )
                                    if metric_data.get('video_link'):
                                        res_cols[1].page_link(
                                            metric_data['video_link'],
                                            label="Video Explanation",
                                            icon="🎥"
                                        )

                            st.markdown("---")

        # ----- Next Steps -----
        st.header("🚦 Next Steps")
        st.markdown("""
        1. **Prioritize 3 Key Actions** from recommendations
        2. **Establish Baseline Metrics** within 7 days
        3. **Create 30/60/90 Day Plan** with milestones
        """)

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise
