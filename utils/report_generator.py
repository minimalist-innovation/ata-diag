import logging
from datetime import datetime
import pandas as pd
import streamlit as st
from db_queries.recommendations import get_recommendations_for_metric
from db_queries.connection import get_db_connection
from utils.ux_helpers import get_progress_column_config

logger = logging.getLogger(__name__)


def render_streamlit_report(session_state):
    """Render diagnostic report with database-powered recommendations"""

    # Validate session state
    required_keys = ['growth_stage_name', 'annual_revenue', 'selected_saas_type',
                     'selected_orientation', 'selected_industry', 'metrics_cache']
    if not all(key in session_state for key in required_keys):
        st.error("❌ Missing critical session data. Please complete the diagnostic first.")
        return

    try:
        # ----- Report Header -----
        st.title("🚀 SaaS Traction Diagnostic Report")
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

        # Get database connection
        conn = get_db_connection()

        try:
            # Group metrics by pillar
            pillars = {}
            for metric_name, metric_data in session_state['metrics_cache'].items():
                pillar_name = metric_data['pillar_name']
                pillars.setdefault(pillar_name, []).append(metric_name)

            # Display metrics by pillar
            for pillar_name, metric_names in pillars.items():
                with st.expander(f"### {pillar_name} Metrics", expanded=True):
                    # Build metrics table
                    metrics_data = []
                    for metric_name in metric_names:
                        metric_data = session_state['metrics_cache'][metric_name]
                        current_value = session_state.get(metric_data["slider_key"], 0)

                        metrics_data.append({
                            "Metric": metric_name,
                            "Current": current_value,  # Store only numeric value
                            "Target": f"{metric_data['target_low_range']}-{metric_data['target_high_range']}{metric_data['unit']}"
                        })

                    # Display metrics table
                    df = pd.DataFrame(metrics_data)
                    st.dataframe(
                        df,
                        column_config={
                            "Metric": st.column_config.TextColumn(width="large"),
                            "Current": get_progress_column_config(metric_data['unit']),
                            "Target": "Target Range"
                        },
                        hide_index=True,
                        use_container_width=True
                    )

                    # Generate recommendations
                    for metric_name in metric_names:
                        metric_data = session_state['metrics_cache'][metric_name]
                        current_value = session_state.get(metric_data["slider_key"], 0)

                        try:
                            current_value = float(str(current_value).rstrip('%'))
                            target_low = float(metric_data['target_low_range'])
                            target_high = float(metric_data['target_high_range'])
                        except ValueError as e:
                            logger.error(f"Value conversion error for {metric_name}: {e}")
                            continue

                        if current_value < target_low or current_value > target_high:
                            with st.container(border=True):
                                # Header
                                st.subheader(f"🚨 {metric_name}")

                                # Current vs Target
                                cols = st.columns([1, 3])
                                with cols[0]:
                                    st.metric("Current", f"{current_value}{metric_data['unit']}")
                                    st.metric("Target", f"{target_low}-{target_high}{metric_data['unit']}")

                                # Recommendations
                                with cols[1]:
                                    recommendations = get_recommendations_for_metric(metric_data['metric_id'])
                                    if recommendations:
                                        st.markdown("#### 🛠 Recommended Actions")
                                        for rec in recommendations:
                                            st.markdown(f"- {rec}")
                                    else:
                                        st.info("No specific recommendations available. Review general best practices.")

                                # Resources
                                st.markdown("#### 📚 Resources")
                                res_cols = st.columns(2)
                                if metric_data.get('blog_link'):
                                    res_cols[0].page_link(metric_data['blog_link'], label="Detailed Guide", icon="📖")
                                if metric_data.get('video_link'):
                                    res_cols[1].page_link(metric_data['video_link'], label="Video Explanation",
                                                          icon="🎥")

                                st.markdown("---")

        finally:
            conn.close()

        # ----- Next Steps -----
        st.header("🚦 Next Steps")
        st.markdown("""
        1. **Prioritize 3 Key Actions** from recommendations above
        2. **Establish Baseline Metrics** within 7 days
        3. **Create 30/60/90 Day Plan** with measurable milestones
        4. **Schedule Follow-up Diagnostic** for %s
        """ % (datetime.now().strftime("%B %d, %Y")))

        st.markdown("---")
        st.caption("Report generated using Adaptive Traction Framework v2.1")

    except KeyError as e:
        logger.error(f"Missing session key: {e}")
        st.error("⚠️ Configuration error. Please restart the diagnostic.")
    except Exception as e:
        logger.error(f"Report generation failed: {e}", exc_info=True)
        st.error("🔥 Critical error generating report. Please contact support.")
