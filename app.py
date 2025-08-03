import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="STEP Diagnostics Tool",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://outlook.office.com/book/MinimalistInnovationLLC@minimalistinnovation.onmicrosoft.com/s/n2ZGHb7DjEq3KeWVxeM4Aw2?ismsaljsauthenabled',
        'Report a bug': "https://www.minimalistinnovation.co/contact",
        'About': "https://www.minimalistinnovation.co/about"
    }
)

from constants import REQUIRED_SESSION_KEYS
from src.components.footer import footer
from src.components.global_assets import load_global_assets
from src.components.header import header


@st.cache_resource
def init_database():
    """Initialize database once per session"""
    try:
        from src.db_queries.db_init import setup_database
        setup_database()
        return True
    except Exception as e:
        st.error(f"Critical error: {str(e)}")
        st.stop()


def initialize_session_state():
    """Initialize required session state variables with defaults"""
    defaults = {
        'selected_saas_type': 'standard_saas',
        'selected_orientation': 'horizontal',
        'selected_industry': 'general_software',
        'annual_revenue': 1.0,
        'growth_stage_id': 0,
        'page_history': [],
        'current_page': None,
    }

    for key in REQUIRED_SESSION_KEYS:
        if key not in st.session_state:
            st.session_state[key] = defaults.get(key, None if key != 'metrics_cache' else {})


if __name__ == "__main__":
    # Initialize
    load_global_assets()
    initialize_session_state()

    # Initialize database connection once
    if 'db_conn' not in st.session_state:
        st.session_state.db_conn = init_database()  # Will be cached

    # Render global header
    header()

    # Configure page navigation
    pages = [
        st.Page(
            "company_profile.py",
            title="Company Profile",
            icon="🏢",
            url_path="company_profile",
            default=not all(st.session_state.get(k) for k in REQUIRED_SESSION_KEYS)
        ),
        st.Page(
            "revenue_metrics.py",
            title="Revenue Metrics",
            icon="💰",
            url_path="revenue_metrics",
        ),
        st.Page(
            "product_metrics.py",
            title="Product Metrics",
            icon="🎁",
            url_path="product_metrics",
        ),
        st.Page(
            "system_metrics.py",
            title="Systems Metrics",
            icon="⚙️",
            url_path="system_metrics",
        ),
        st.Page(
            "people_metrics.py",
            title="People Metrics",
            icon="🧑‍🤝‍🧑",
            url_path="people_metrics",
        ),
        st.Page(  # Add Report Page
            "report_page.py",
            title="Generate Report",
            icon="📊",
            url_path="report",
        )
    ]

    # Create navigation controller
    nav = st.navigation(
        pages,
        position="sidebar",
        expanded=False
    )

    # Execute selected page
    nav.run()

    # Render global footer
    footer()
