import streamlit as st

from src.components.pillar_template import pillar_page_template

# Set pillar ID and call template
PILLAR_ID = 2


def main():
    """Main entry point for product pillar page"""

    # Navigation guard
    if 'pillar_1_complete' not in st.session_state:
        st.error("Complete Company Profile First")
        st.switch_page("company_profile.py")
        return

    pillar_page_template(PILLAR_ID)


if __name__ == "__main__":
    main()
