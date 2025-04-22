import os
import sys
import sqlite3
import importlib.util
import streamlit as st
import streamlit.components.v1 as components

import html
import logging
import toml

from datetime import datetime
from db_queries.saas_types import get_saas_types
from db_queries.orientations import get_orientations
from db_queries.industries import get_industries
from db_queries.growth_stages import determine_company_stage
from db_queries.connection import get_db_connection
from utils.slider_helpers import get_slider_format, get_slider_range, get_step_size


# Load and use Streamlit config
def setup_logging():
    """Configure logging based on .streamlit/config.toml settings"""
    try:
        # Attempt to load the config.toml file
        config_path = os.path.join('.streamlit', 'config.toml')
        if os.path.exists(config_path):
            config = toml.load(config_path)

            # Get logging settings from config
            log_level = config.get('logger', {}).get('level', 'info').upper()
            log_format = config.get('logger', {}).get('messageFormat',
                                                      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Check if file logging is enabled
            enable_file_logging = config.get('logger', {}).get('enableFileLogging', False)
            log_file_path = config.get('logger', {}).get('logFilePath', 'logs/app.log')

            # Convert string level to logging level
            level_map = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL
            }
            level = level_map.get(log_level, logging.INFO)

            # Configure basic logging
            logging.basicConfig(level=level, format=log_format)

            # Add file handler if enabled
            if enable_file_logging:
                # Ensure log directory exists
                log_dir = os.path.dirname(log_file_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                # Add file handler
                file_handler = logging.FileHandler(log_file_path)
                file_handler.setFormatter(logging.Formatter(log_format))

                # Add to root logger
                root_logger = logging.getLogger()
                root_logger.addHandler(file_handler)

            return True
        else:
            # Fall back to basic config if no file exists
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            return False
    except Exception as e:
        # If anything goes wrong, fall back to basic config
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.error(f"Error setting up logging from config: {str(e)}")
        return False


# Set up logging from config
config_loaded = setup_logging()
logger = logging.getLogger(__name__)

if config_loaded:
    logger.info("Logging configured from .streamlit/config.toml")
else:
    logger.info("Using default logging configuration")

# === Page Configuration ===
st.set_page_config(
    page_title="Adaptive Traction Architecture Diagnostics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# === Custom Theme & Styling ===
# Try to load colors from config or use defaults
try:
    config_path = os.path.join('.streamlit', 'config.toml')
    if os.path.exists(config_path):
        config = toml.load(config_path)
        color_config = config.get('colors', {})

        # Get colors from config or use defaults
        primary_color = color_config.get('primaryColor', "#233292")
        secondary_color = color_config.get('secondaryColor', "#26619C")
        tertiary_color = color_config.get('tertiaryColor', "#385424")
        quaternary_color = color_config.get('quaternaryColor', "#4D466B")
        highlight_color = color_config.get('highlightColor', "#AC2147")
        link_color = color_config.get('linkColor', "#00A8A8")
    else:
        # Default colors
        primary_color = "#233292"  # Deep blue
        secondary_color = "#26619C"  # Medium blue
        tertiary_color = "#385424"  # Forest green
        quaternary_color = "#4D466B"  # Purple-gray
        highlight_color = "#AC2147"  # Red highlight
        link_color = "#00A8A8"  # Teal for hyperlinks
except Exception as e:
    logger.warning(f"Could not load colors from config, using defaults: {str(e)}")
    # Default colors
    primary_color = "#233292"  # Deep blue
    secondary_color = "#26619C"  # Medium blue
    tertiary_color = "#385424"  # Forest green
    quaternary_color = "#4D466B"  # Purple-gray
    highlight_color = "#AC2147"  # Red highlight
    link_color = "#00A8A8"  # Teal for hyperlinks


# Load CSS Dynamically
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load Javascript dynamically
def load_js(file_path):
    with open(file_path) as f:
        js_code = f.read()
        components.html(f"<script>{js_code}</script>", height=0)


def add_toolbar():
    st.markdown("""
    <style>
        /* Hide Streamlit's default header and menu */
        header, #MainMenu, footer {visibility: hidden;}
    
        /* Remove top margin/padding */
        .block-container { padding-top: 0 !important; margin-top: 0 !important; }
        .css-18e3th9 { padding-top: 0 !important; } /* Sometimes needed for newer Streamlit */
    </style>
    """, unsafe_allow_html=True)

    app_toolbar_html = f"""
    <div class="top-toolbar">
        <span class="toolbar-text">Need Clarity?</span>
        <a href="https://outlook.office.com/owa/calendar/MinimalistInnovationLLC@minimalistinnovation.onmicrosoft.com/bookings/s/H_o18Z1ej0OAvMiMMMyhTA2" 
            class="toolbar-cta" 
            target="_blank">
            🤙Schedule a Call Now
        </a>
    </div>
    <div class="toolbar-spacer"></div>
    """
    st.markdown(app_toolbar_html, unsafe_allow_html=True)


# === Helper Functions ===
def add_logo():
    try:
        # Create a container with two columns
        col1, col2 = st.columns([3, 1])

        with col1:
            # Left side: App logo (existing)
            app_logo_html = f"""
            <div style="display: flex; align-items: center;">
                <div style="background-color: {primary_color}; width: 40px; height: 40px; border-radius: 8px; 
                          display: flex; justify-content: center; align-items: center; margin-right: 12px;">
                    <span style="color: white; font-weight: bold; font-size: 18px;">ATA</span>
                </div>
                <div>
                    <h2 style="margin: 0; padding: 0; color: {primary_color};">Adaptive Traction Architecture</h2>
                    <h3 style="margin: 0; padding: 0; color: {primary_color};"> Diagnostics</h3>
                </div>
            </div>
            """
            st.markdown(app_logo_html, unsafe_allow_html=True)

        with col2:
            # Right side: Company logo using st.image
            import os
            from PIL import Image

            # Path to your SVG logo
            logo_path = os.path.join("media", "Minimalist_Horizontal_Blue.svg")

            # Display the logo - align it to the right
            st.image(logo_path, width=200)  # Adjust width as needed

        logger.debug("Logos rendered successfully")
    except Exception as e:
        logger.error(f"Error displaying logos: {str(e)}")
        st.error(f"Error displaying logos: {str(e)}")


def import_and_setup_database():
    """Import the setup_database module and run the setup function"""
    try:
        # Check if setup_database.py exists
        if not os.path.exists('setup_database.py'):
            logger.error("setup_database.py file not found")
            st.error("setup_database.py file not found. Please ensure it's in the same directory as app.py.")
            st.stop()

        # Import the module dynamically
        spec = importlib.util.spec_from_file_location("setup_database", "setup_database.py")
        setup_db_module = importlib.util.module_from_spec(spec)
        sys.modules["setup_database"] = setup_db_module
        spec.loader.exec_module(setup_db_module)

        logger.info("Successfully imported setup_database module")

        # Run the setup function
        setup_db_module.setup_database()
        logger.info("Database setup completed")
    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        st.error(f"Error setting up database: {str(e)}")
        st.stop()


def query_problems_by_pillar_and_stage(pillar, stage_name):
    """Query problems for a specific pillar and growth stage

    Args:
        pillar: One of "Product", "Business", "Systems", "Team"
        stage_name: One of the growth stage names (e.g., "Validation Seekers")

    Returns:
        List of problem dictionaries
    """
    logger.debug(f"Querying problems for pillar: {pillar}, stage: {stage_name}")
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT *
                       FROM architecture_problems
                       WHERE architecture_pillar = ?
                         AND growth_stage_name = ?
                       ''', (pillar, stage_name))

        results = [dict(row) for row in cursor.fetchall()]
        logger.debug(f"Found {len(results)} problems for {pillar} in {stage_name}")
        return results
    except sqlite3.Error as e:
        logger.error(f"Error querying problems: {str(e)}")
        st.error(f"Error retrieving metrics: {str(e)}")
        return []
    finally:
        conn.close()


def display_metrics_for_pillar(pillar, growth_stage):
    """Display metric sliders for a specific pillar and growth stage"""
    # Get problems/metrics for this pillar and growth stage
    problems = query_problems_by_pillar_and_stage(pillar, growth_stage)

    if not problems:
        logger.warning(f"No metrics found for {pillar} in {growth_stage} stage")
        st.write(f"No metrics found for {pillar} in {growth_stage} stage.")
        return

    # Display each metric with a slider
    for problem in problems:
        # Escape the metric name and problem description
        metric_name = html.escape(problem['metric_name'])
        problem_description = html.escape(problem['problem_description'])

        # Display the metric name and problem description with bold for the metric name
        st.markdown(f"**{metric_name}**")
        st.markdown(f"{problem_description}")

        # Create a unique key for each slider
        slider_key = f"{pillar}_{problem['id']}_{problem['metric_name']}"

        # Get appropriate format and range for this metric
        slider_format = get_slider_format(problem['metric_name'])
        min_val, max_val = get_slider_range(problem['metric_name'])
        step_size = get_step_size(problem['metric_name'])

        # Determine default value based on the rules
        if min_val != problem['low_range']:
            default_value = problem['low_range']
        elif max_val != problem['hi_range']:
            default_value = problem['hi_range']
        else:
            # If no special case, use the midpoint or appropriate default
            if "CAC trend" in problem['metric_name']:
                default_value = 0.0  # Default to flat for CAC trend
            else:
                default_value = (problem['low_range'] + problem['hi_range']) / 2

        # Ensure default is within bounds
        default_value = max(min_val, min(max_val, default_value))

        logger.debug(f"Creating slider for metric: {metric_name}, range: {min_val}-{max_val}, default: {default_value}")

        # Create the slider with appropriate format
        value = st.slider(
            f"**Current value**",
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(default_value),
            step=step_size,
            format=slider_format,
            key=slider_key
        )

        st.markdown("---")


# === App Layout ===
def main():
    try:
        logger.debug("Starting Adaptive Traction Architecture Diagnostics app")

        # Load all the assets
        load_css("static/styles.css")
        load_js("static/script.js")

        # Add the toolbar
        add_toolbar()
        # Add logo
        add_logo()

        # Basic interactivity for demo purposes
        st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)

        # Determine the SaaS Classification
        st.header("Company Information")

        # SaaS Type Selection
        saas_types = get_saas_types()
        selected_saas_type = st.selectbox(
            "Select your SaaS company type:",
            options=saas_types,
            format_func=lambda x: x['type_name']
        )

        # Orientation Selection
        orientations = get_orientations()
        selected_orientation = st.selectbox(
            "Is your company Horizontal or Vertical SaaS?",
            options=orientations,
            format_func=lambda x: x['orientation_name']
        )

        industries = get_industries(selected_saas_type['id'], selected_orientation['id'])
        if not industries:
            st.error("No valid industries found for this combination. Please check your previous selections.")
            return

        selected_industry = st.selectbox(
            "Select your primary industry/sector:",
            options=industries,
            format_func=lambda x: x['industry_name']
        )

        # Ask for company existence duration
        months_existed = st.number_input("How long has your company been in existence? (months)",
                                         min_value=1, max_value=240, value=12)
        logger.debug(f"Company existence duration input: {months_existed} months")

        # Revenue input based on company age
        if months_existed < 24:
            # For newer companies, ask for MRR and convert to ARR
            mrr = st.slider("**Monthly Recurring Revenue (MRR in \\$K)**",
                            min_value=0.0,
                            max_value=1000.0,
                            value=83.33,  # This equals ~$1M ARR
                            step=20.83,  # This equals ~$250K ARR (0.25M)
                            format="$%.2fK")

            # Convert MRR (in thousands) to ARR (in millions)
            annual_revenue = (mrr * 12) / 1000
            logger.debug(f"MRR input: ${mrr}K, converted to ARR: ${annual_revenue}M")

            # Display the converted ARR value
            st.info(f"**Your estimated Annual Recurring Revenue (ARR): __\\${annual_revenue:.2f}M__**")
        else:
            # For established companies, ask directly for ARR
            annual_revenue = st.slider("**Annual Recurring Revenue (ARR in \\$M)**",
                                       min_value=0.0,
                                       max_value=12.0,
                                       value=1.5,
                                       step=0.25,
                                       format="$%.2fM")
            logger.debug(f"ARR input: ${annual_revenue}M")

        # Warning for revenue > 10M
        if annual_revenue > 10.0:
            logger.info(f"ARR exceeds $10M: ${annual_revenue}M")
            st.warning(
                "Your revenue exceeds \\$10M ARR. This diagnostic tool is primarily designed for companies in the \\$1M-\\$10M ARR range. Some insights may not apply to your current scale.")

        # Determine company stage using the database
        stage, explanation = determine_company_stage(annual_revenue)

        # Display stage with styling based on qualification
        if stage == "Pre-Qualification":
            logger.info(f"Company stage determined as Pre-Qualification (ARR: ${annual_revenue}M)")
            st.markdown(f"<div class='error'><strong>Company Stage: {stage}</strong><br>{explanation}</div>",
                        unsafe_allow_html=True)
        else:
            logger.info(f"Company stage determined as {stage} (ARR: ${annual_revenue}M)")
            st.markdown(f"<div class='success'><strong>Company Stage: {stage}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info'>{explanation}</div>", unsafe_allow_html=True)

            # Only show diagnostic options if qualified
            if stage != "Pre-Qualification":
                st.markdown("<h4>Four Pillars of Adaptive Traction Architecture</h4>", unsafe_allow_html=True)

                # Create tabs for the four pillars
                logger.debug("Creating pillar tabs")
                pillars_tabs = st.tabs(["Business/Revenue", "Product", "Systems", "Team"])

                # Business pillar tab
                with pillars_tabs[0]:
                    st.markdown(
                        "**Evaluates your acquisition channels, pricing strategy, customer journey, and revenue resilience to identify patterns limiting growth or creating vulnerability to market shifts.**")

                    logger.debug("Displaying Business pillar metrics")
                    display_metrics_for_pillar("Business", stage)

                # Product pillar tab
                with pillars_tabs[1]:
                    st.markdown(
                        "**Assesses your product development approach, feedback mechanisms, feature adoption patterns, and market responsiveness to reveal gaps between product evolution and market needs.**")

                    logger.debug("Displaying Product pillar metrics")
                    display_metrics_for_pillar("Product", stage)

                # Systems pillar tab
                with pillars_tabs[2]:
                    st.markdown(
                        "**Examines your operational processes, technology infrastructure, data accessibility, and technical debt to identify inefficiencies and scalability constraints.**")

                    logger.debug("Displaying Systems pillar metrics")
                    display_metrics_for_pillar("Systems", stage)

                # Team pillar tab
                with pillars_tabs[3]:
                    st.markdown(
                        "**Explores your decision-making frameworks, information flow patterns, organizational structure, and change management capabilities to uncover bottlenecks limiting adaptive capacity.**")

                    logger.debug("Displaying Team pillar metrics")
                    display_metrics_for_pillar("Team", stage)

                disclaimer_text = f"""
                This tool is provided for informational and experimental purposes only and is provided 'as is' without warranties of any kind.
                Do not rely solely on the results for business decisions. Always consult with a qualified expert before taking action based on these diagnostics.
                Use of this tool is at your own risk.
                """
                st.warning(
                    disclaimer_text,
                    icon="⚠️"
                )

                if st.button("Run Diagnostics", type="primary"):
                    logger.info("Run Diagnostics button clicked")
                    st.success("Diagnostic analysis complete!")

        st.markdown("</div>", unsafe_allow_html=True)

        # Horizontal line
        st.markdown("---")

        # Copyright footer with dynamically generated year
        # Add a spacer to prevent content from being hidden behind the fixed footer
        st.markdown("<div class='footer-spacer'></div>", unsafe_allow_html=True)

        # Copyright footer with dynamically generated year
        current_year = datetime.now().year
        st.markdown(f"""
        <div class="footer">
            © {current_year} Minimalist Innovation LLC. All rights reserved.
        </div>
        """, unsafe_allow_html=True)
        logger.info("App rendered successfully")

    except Exception as e:
        logger.error(f"An error occurred in the main app flow: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again.")


if __name__ == '__main__':
    try:
        # Make sure the database is set up
        import_and_setup_database()
        main()
    except Exception as e:
        logger.critical(f"Fatal error in app startup: {str(e)}", exc_info=True)
        st.error(f"Fatal error: {str(e)}")
