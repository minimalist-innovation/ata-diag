import streamlit as st

from src.components.pillar_template import pillar_page_template

# Set pillar ID and call template
PILLAR_ID = 1


def main():
    """Main entry point for revenue pillar page"""
    st.session_state.current_page = "revenue_metrics.py"

    # Navigation guard
    if not all(st.session_state.get(k) for k in ['selected_saas_type', 'selected_orientation']):
        st.error("Complete Revenue Metrics First")
        st.switch_page("revenue_metrics.py")
        return

    pillar_page_template(PILLAR_ID)


if __name__ == "__main__":
    main()
