# pages/report_page.py

import streamlit as st

from constants import REQUIRED_SESSION_KEYS
from src.components.cta_toast import show_sequential_cta_toasts
from src.components.report import generate_report


def main():
    """Main entry point for report generation page"""
    if not all(key in st.session_state for key in REQUIRED_SESSION_KEYS):
        st.error("Complete company profile first")
        st.switch_page("company_profile.py")

    try:
        # Validate session state before rendering
        required_keys = [
            'growth_stage_name',
            'annual_revenue',
            'selected_saas_type',
            'selected_orientation',
            'selected_industry',
            'pillar_1_complete',
            'pillar_2_complete',
            'pillar_3_complete'
        ]

        if not all(key in st.session_state for key in required_keys):
            st.error("❌ Complete all previous steps before generating report")
            st.page_link("company_profile.py", label="← Return to Company Profile")
            return

        # Generate the report
        show_sequential_cta_toasts()  # Display CTA toasts
        with st.spinner("🔍 Generating your personalized report..."):
            st.session_state.page_history.append(st.session_state.current_page)
            generate_report(st.session_state)

    except Exception as e:
        st.error(f"Report generation failed: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()
