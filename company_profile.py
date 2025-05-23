import logging

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

from constants import REQUIRED_SESSION_KEYS
from src.db_queries.growth_stages import determine_company_stage
from src.db_queries.industries import get_industries, get_all_industries
from src.db_queries.orientations import get_orientations
from src.db_queries.saas_types import get_saas_types

logger = logging.getLogger(__name__)


def main():
    # --- Initialize all required session keys ---
    for key in REQUIRED_SESSION_KEYS:
        if key not in st.session_state:
            if key == 'metrics_cache':
                st.session_state[key] = {}
            else:
                st.session_state[key] = None

    st.session_state.current_page = "company_profile.py"
    st.session_state.page_history.append("company_profile.py")
    st.title("🏢 Company Profile")
    st.markdown("Please enter your company details to begin your diagnostics.")

    # --- Layout ---
    left_gutter, main_content, right_gutter = st.columns([0.05, 0.9, 0.05], gap="small")
    with main_content:
        col1, col2 = st.columns(2, gap="medium")

        # --- Column 1: SaaS Type and Orientation ---
        with col1:
            saas_types = get_saas_types()
            saas_types_with_all = {None: {'type_name': 'All SaaS Types'}}
            saas_types_with_all.update(saas_types)
            selected_saas_type = st.selectbox(
                "Select your SaaS company type:",
                index=0,
                options=list(saas_types_with_all.keys()),
                format_func=lambda x: saas_types_with_all[x]['type_name'] if x is not None else 'All SaaS Types',
                key="selected_saas_type_key"
            )
            st.session_state['selected_saas_type'] = saas_types_with_all[selected_saas_type]['type_name']

            orientations = get_orientations()
            selected_orientation = st.selectbox(
                "Is your company Horizontal or Vertical SaaS?",
                index=0,
                options=list(orientations.keys()),
                format_func=lambda x: orientations[x]['orientation_name'],
                key="selected_orientation_key"
            )
            st.session_state['selected_orientation'] = orientations[selected_orientation]['orientation_name']

        # --- Column 2: Industry, Age, Revenue ---
        with col2:
            if selected_saas_type is None or selected_orientation is None:
                industries = get_all_industries()
            else:
                industries = get_industries(selected_saas_type, selected_orientation)
            if not industries:
                st.error("No valid industries found for this combination. Please check your previous selections.")
                st.session_state['selected_industry'] = None
                st.session_state['annual_revenue'] = None
                st.session_state['growth_stage_id'] = None
                return

            industries_with_all = {None: {'industry_name': 'All Industries'}}
            industries_with_all.update(industries)
            selected_industry = st.selectbox(
                "Select your primary industry/sector:",
                index=0,
                options=list(industries_with_all.keys()),
                format_func=lambda x: industries_with_all[x]['industry_name'] if x is not None else 'All Industries',
                key="selected_industry_key"
            )
            st.session_state['selected_industry'] = industries_with_all[selected_industry]['industry_name']

            months_existed = st.number_input(
                "How long has your company been in existence? (months)",
                min_value=1, max_value=240, value=12, key="months_existed_key"
            )

            # --- Revenue input ---
            if months_existed < 24:
                mrr = st.slider(
                    "**Monthly Recurring Revenue (MRR in \\$K)**",
                    min_value=0.0, max_value=1000.0, value=83.33, step=20.83,
                    format="$%.2fK", key="mrr_key"
                )
                annual_revenue = (mrr * 12) / 1000  # in millions
                add_vertical_space(3)
                st.info(f"**Your estimated Annual Recurring Revenue (ARR): __\\${annual_revenue:.2f}M__**")
            else:
                annual_revenue = st.slider(
                    "**Annual Recurring Revenue (ARR in \\$M)**",
                    min_value=0.0, max_value=12.0, value=1.5, step=0.25,
                    format="$%.2fM", key="arr_key"
                )
                add_vertical_space(3)
                if annual_revenue > 10.0:
                    st.warning(
                        "Your revenue exceeds \\$10M ARR. This diagnostic tool is primarily designed for companies in the \\$1M-\\$10M ARR range. Some insights may not apply to your current scale."
                    )

            st.session_state['annual_revenue'] = annual_revenue

        # --- Determine and store company stage ---
        stage_data = determine_company_stage(annual_revenue)
        if not stage_data:
            stage_id = None
            stage_name = "Undetermined"
            stage_description = "Could not determine company stage"
        else:
            stage_id = next(iter(stage_data))
            stage_info = stage_data[stage_id]
            stage_name = stage_info['growth_stage_name']
            stage_description = stage_info['description']

        st.session_state["growth_stage_id"] = stage_id
        st.session_state["growth_stage_name"] = stage_name

        # --- Display stage ---
        if stage_name == "Pre-Qualification":
            st.markdown(f"<div class='error'><strong>Company Stage: {stage_name}</strong></div>",
                        unsafe_allow_html=True)
            st.markdown(f"<div class='disqualinfo'>{stage_description}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='success'><strong>Company Stage: {stage_name}</strong></div>",
                        unsafe_allow_html=True)
            st.markdown(f"<div class='info'>{stage_description}</div>", unsafe_allow_html=True)

            # --- Check if all required fields are filled ---
            required_fields = [
                'selected_saas_type',
                'selected_orientation',
                'selected_industry',
                'annual_revenue',
                'growth_stage_id',
                'growth_stage_name'
            ]

            all_filled = all(st.session_state.get(field) for field in required_fields)

            nav_col1, spacer, nav_col3 = st.columns([2, 1, 2])
            with nav_col3:
                if all_filled:
                    if st.button("Continue ▶",
                                 type="primary",
                                 key="company_profile_continue"):
                        st.session_state['company_profile_complete'] = True
                        st.session_state.page_history.append("revenue_metrics.py")
                        st.session_state.current_page = "revenue_metrics.py"
                        st.switch_page("revenue_metrics.py")
                else:
                    st.info("Please complete all fields above to continue.")


if __name__ == "__main__":
    main()
