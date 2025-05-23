import logging

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

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

        col1, spacer, col3 = st.columns([2, 1, 2])
        with col1:
            with stylable_container(
                    key="back_group_container",
                    css_styles="""
                               button {
                                    float: left;
                                    margin-left: auto;
                                }
                                .left-stack {
                                    display: flex;
                                    flex-direction: column;
                                    align-items: flex-start; /* left-align both caption and button */
                                }
                                .left-stack .caption {
                                    color: gray;
                                    font-style: italic;
                                    font-size: 0.875rem;
                                    margin-bottom: 0.75rem; /* adjust spacing as needed */
                                }
                                """
            ):
                if len(st.session_state.page_history) > 0:
                    st.markdown(
                        """
                        <div class="left-stack">
                            <div class="caption">
                                Previous: {0}
                            </div>
                        </div>
                        """.format(previous_page.replace('_', ' ').title()[:-3]), unsafe_allow_html=True)
                    st.markdown('<div class="left-stack">', unsafe_allow_html=True)
                    if st.button("◀︎ Back",
                                 type="primary",
                                 key=f"pillar_{pillar_id}_back"):
                        # Pop current page from history and switch to previous
                        st.session_state.page_history.pop()  # Remove current
                        session_previous_page = st.session_state.page_history[-1]
                        st.session_state.current_page = session_previous_page
                        st.switch_page(session_previous_page)
                    st.markdown("</div>", unsafe_allow_html=True)

        # Spacer column, leave empty
        with spacer:
            pass

        with col3:
            with stylable_container(
                    key="continue_group_container",
                    css_styles="""
                   button {
                        float: right;
                        margin-left: auto;
                    }
                    .right-stack {
                        display: flex;
                        flex-direction: column;
                        align-items: flex-end; /* right-align both caption and button */
                    }
                    .right-stack .caption {
                        color: gray;
                        font-style: italic;
                        font-size: 0.875rem;
                        margin-bottom: 0.75rem; /* adjust spacing as needed */
                    }
                    """
            ):
                st.markdown(
                    """
                    <div class="right-stack">
                        <div class="caption">
                            Next: {0}
                        </div>
                    </div>
                    """.format(next_page.replace('_', ' ').title()[:-3]), unsafe_allow_html=True)

                st.markdown('<div class="right-stack">', unsafe_allow_html=True)
                if st.button("Continue ▶︎",
                             type="primary",
                             key=f"pillar_{pillar_id}_continue"):
                    # Update history before switching
                    st.session_state.page_history.append(next_page)
                    st.session_state.current_page = next_page
                    st.session_state[f"pillar_{pillar_id}_complete"] = True
                    st.switch_page(next_page)
                st.markdown("</div>", unsafe_allow_html=True)


    except Exception as e:
        logger.error(f"Pillar page error: {str(e)}")
        st.error("Error loading pillar metrics")
