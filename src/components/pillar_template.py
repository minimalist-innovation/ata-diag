import logging

import streamlit as st

from src.components.metrics import display_metrics_for_pillar
from src.db_queries.architecture_pillars import get_architecture_pillars

logger = logging.getLogger(__name__)


def pillar_page_template(pillar_id: int):
    """Reusable template for all pillar pages"""
    try:
        # Get pillar metadata
        pillars_data = get_architecture_pillars()
        pillar_data = pillars_data.get(pillar_id)

        if not pillar_data:
            st.error("Invalid pillar configuration")
            logger.error(f"Pillar ID {pillar_id} not found in pillars data")
            return

        # Verify required session state exists
        required_keys = ['growth_stage_id', 'selected_saas_type', 'selected_industry']
        missing_keys = [key for key in required_keys if key not in st.session_state]

        if missing_keys:
            st.error(f"Missing required company data: {', '.join(missing_keys)}")
            st.page_link("company_profile.py", label="← Return to Company Profile", icon="🏠")
            logger.warning(f"Missing session keys: {missing_keys}")
            return

        # Page header
        st.title(f"{pillar_data['display_icon']} {pillar_data['pillar_name']} Metrics")
        st.caption(pillar_data['description'])

        # Display metrics
        display_metrics_for_pillar(
            architecture_pillar_id=pillar_id,
            growth_stage_id=st.session_state['growth_stage_id'],
            saas_type_id=st.session_state.get('selected_saas_type'),
            industry_id=st.session_state.get('selected_industry')
        )

        next_page = {
            0: "company_profile.py",
            1: "revenue_metrics.py",
            2: "product_metrics.py",
            3: "system_metrics.py",
            4: "people_metrics.py",
            5: "report_page.py"
        }.get(pillar_id + 1)
        previous_page = {
            0: "company_profile.py",
            1: "revenue_metrics.py",
            2: "product_metrics.py",
            3: "system_metrics.py",
            4: "people_metrics.py",
            5: "report_page.py"
        }.get(pillar_id - 1)

        nav_col1, spacer, nav_col3 = st.columns([2, 1, 2])
        with nav_col1:
            if len(st.session_state.page_history) > 0:
                st.caption(f"Previous: {previous_page.replace('_', ' ').title()[:-3]}")
                if st.button("◀︎ Back",
                             type="primary",
                             key=f"pillar_{pillar_id}_back"):
                    # Pop current page from history and switch to previous
                    st.session_state.page_history.pop()  # Remove current
                    session_previous_page = st.session_state.page_history[-1]
                    st.session_state.current_page = session_previous_page
                    st.switch_page(session_previous_page)
        with nav_col3:
            st.caption(f"Next: {next_page.replace('_', ' ').title()[:-3]}")
            if st.button("Continue ▶︎",
                         type="primary",
                         key=f"pillar_{pillar_id}_continue"):
                # Update history before switching
                st.session_state.page_history.append(next_page)
                st.session_state.current_page = next_page
                st.session_state[f"pillar_{pillar_id}_complete"] = True
                st.switch_page(next_page)

    except Exception as e:
        logger.error(f"Pillar page error: {str(e)}")
        st.error("Error loading pillar metrics")
