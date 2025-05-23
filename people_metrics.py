import streamlit as st

from src.components.pillar_template import pillar_page_template

# Set pillar ID and call template
PILLAR_ID = 4


def main():
    """Main entry point for people pillar page"""
    st.session_state.current_page = "people_metrics.py"

    # Navigation guard
    if 'pillar_3_complete' not in st.session_state:
        st.error("Complete Systems Metrics First")
        st.switch_page("system_metrics.py")
        return

    pillar_page_template(PILLAR_ID)


if __name__ == "__main__":
    main()
