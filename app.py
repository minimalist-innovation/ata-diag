import os
import sys
import importlib.util
import streamlit as st
from streamlit import cache_data, cache_resource
import logging
import toml
import base64
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from datetime import datetime
from db_queries.saas_types import get_saas_types
from db_queries.orientations import get_orientations
from db_queries.industries import get_industries
from db_queries.architecture_pillars import get_architecture_pillars
from db_queries.growth_stages import determine_company_stage
from db_queries.metrics import get_metrics
from utils.slider_helpers import get_slider_format, get_step_size
from utils.ux_helpers import add_toolbar, add_logo, load_css, load_js, add_footer


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
    page_icon="💸",
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


def import_and_setup_database():
    """Import and run database setup once"""
    try:
        from setup_database import setup_database
        setup_database()
        logger.info("Database setup completed")
        st.session_state.db_init = True  # Mark as initialized
    except Exception as e:
        logger.error(f"Database setup failed: {str(e)}")
        st.error(f"Critical error: {str(e)}")
        st.stop()


def init_session_state():
    """Initialize persistent session variables only"""
    if 'db_init' not in st.session_state:
        st.session_state.update({
            'db_init': True,
            'metrics_cache': {},
            'pillar_data': None,
            'selected_saas_type': None,
            'selected_orientation': None,
            'selected_industry': None
        })

        # One-time database setup check
        if not os.path.exists('data/traction_diagnostics.db'):
            import_and_setup_database()


def display_metrics_for_pillar(architecture_pillar_id,
                               growth_stage_id,
                               saas_type_id=None,
                               industry_id=None):
    logger.info(f"Displaying metrics for pillar {architecture_pillar_id}, growth stage {growth_stage_id}")

    # Get metrics dictionary with ID keys
    metrics_dict = get_metrics(
        growth_stage_id=growth_stage_id,
        architecture_pillar_id=architecture_pillar_id,
        saas_type_id=saas_type_id,
        industry_id=industry_id
    )

    if not metrics_dict:
        logger.warning(f"No metrics found for pillar ID {architecture_pillar_id} in stage ID {growth_stage_id}")
        st.write(f"No metrics found for this combination.")
        return

    # Get pillar name for display purposes
    pillar_name = get_architecture_pillars().get(architecture_pillar_id, {}).get('pillar_name',
                                                                                 f"Pillar {architecture_pillar_id}")
    # Display each metric using dictionary values
    for metric_id, metric in metrics_dict.items():
        logger.info(f"Trying to display metric for pillar {architecture_pillar_id}: "
                    f"{metric['metric_name']}")
        container = st.container(border=True)

        with container:
            # Video hover functionality
            if metric['video_link']:
                video_url = metric['video_link'].replace('watch?v=', 'embed/')
                with st.popover("📹 Video Guide", help="Click for video tutorial"):
                    st.video(video_url)

            # Metric header
            st.markdown(f"### {metric['metric_name']}")

            # Description with read more
            short_desc = ' '.join(metric['description'].split()[:10]) + '...'
            if metric['blog_link']:
                st.markdown(f"{short_desc} [Read More]({metric['blog_link']})")
            else:
                st.markdown(short_desc)

            # Slider configuration
            slider_key = f"{pillar_name}_{metric_id}_{metric['metric_name']}"
            slider_format = get_slider_format(metric['units'])
            min_val = float(metric['min_value'])
            max_val = float(metric['max_value'])
            step_size = get_step_size(metric['units'])

            # Slider with improved labeling
            target_range = f"**_{metric['lo_range_value']} - {metric['hi_range_value']} {metric['units']}_**"
            current_value = st.slider(
                label=f"The target range is [{target_range}]. What is your value:",
                min_value=min_val,
                max_value=max_val,
                value=(float(metric['lo_range_value']) + float(metric['hi_range_value'])) / 2,
                step=step_size,
                format=slider_format,
                key=slider_key
            )

        st.markdown("---")


def save_architecture_problems_metrics_input():
    """Save architecture problems metrics inputs to memory"""
    metrics_data = []

    # Iterating widget data from session state and creating metrics_data from it
    for key, value in st.session_state.items():
        metric_data = []

        # spliting widget key to get the metric names
        for name in key.split("_"):
            if not name.isdigit():
                metric_data.append(name)
        
        metric_data.append(value)
        metrics_data.append(metric_data)

    return metrics_data


def generate_pdf_report(metrics_data):
    """ generate PDF report format from given metrics data"""
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.spaceAfter = 6
    
    # Build the PDF content
    content = []
    
    # Report header
    content.append(Paragraph("Diagnostic Report", title_style))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Architecture_problems_metrics information section
    content.append(Paragraph("Metrics Information", heading_style))
    
    # Get all metrics data
    report_data = [
        ["Architecture Pillar", "Growth Stage", "Metric", "Metric Value"]
    ]

    for metric_info in metrics_data:
        report_data.append(metric_info)

    table = Table(report_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    content.append(table)
    content.append(Spacer(1, 0.1*inch))

    # Build the PDF
    doc.build(content)
    buffer.seek(0)
    
    return buffer


def get_pdf_download_link(pdf_buffer, filename="Diagnostic_report.pdf"):
    """Function to generate downloadable link for PDF"""
    b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF Report</a>'
    return href


# === App Layout ===
def main():
    try:
        logger.debug("Rendering UI components")

        # Basic interactivity for demo purposes
        st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)

        # Determine the SaaS Classification
        st.header("Company Information")

        # SaaS Type Selection
        saas_types = get_saas_types()
        selected_saas_type = st.selectbox(
            "Select your SaaS company type:",
            options=saas_types.keys(),
            format_func=lambda x: saas_types[x]['type_name']
        )

        # Orientation Selection
        orientations = get_orientations()
        selected_orientation = st.selectbox(
            "Is your company Horizontal or Vertical SaaS?",
            options=orientations.keys(),
            format_func=lambda x: orientations[x]['orientation_name']
        )

        industries = get_industries(selected_saas_type, selected_orientation)
        if not industries:
            st.error("No valid industries found for this combination. Please check your previous selections.")
            return
        selected_industry = st.selectbox(
            "Select your primary industry/sector:",
            options=industries.keys(),
            format_func=lambda x: industries[x]['industry_name']
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
        current_stage = None
        stage_data = determine_company_stage(annual_revenue)
        # Handle case where no matching stage found
        if not stage_data:
            stage_name = "Undetermined"
            stage_description = "Could not determine company stage"
        else:
            # Extract first (and only) entry from the dictionary
            stage_id = next(iter(stage_data))  # Get the dictionary key (stage ID)
            current_stage = stage_id
            stage_info = stage_data[stage_id]  # Get the nested stage info
            stage_name = stage_info['growth_stage_name']
            stage_description = stage_info['description']

        # Display stage with styling based on qualification
        if stage_name == "Pre-Qualification":
            logger.info(f"Company stage determined as Pre-Qualification (ARR: ${annual_revenue}M)")
            st.markdown(f"<div class='error'><strong>Company Stage: {stage_name}</strong><br>{stage_description}</div>",
                        unsafe_allow_html=True)
        else:
            logger.info(f"Company stage determined as {stage_name} (ARR: ${annual_revenue}M)")
            st.markdown(f"<div class='success'><strong>Company Stage: {stage_name}</strong></div>",
                        unsafe_allow_html=True)
            st.markdown(f"<div class='info'>{stage_description}</div>", unsafe_allow_html=True)

            # Only show diagnostic options if qualified
            if stage_name != "Pre-Qualification":
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
                    metrics_data = save_architecture_problems_metrics_input()
                    logger.info("Run Diagnostics button clicked")
                    st.success("Diagnostic analysis complete!")

                    # Generate PDF report
                    pdf_buffer = generate_pdf_report(metrics_data)
                    filename = f"Diagnostic_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                        
                    # Create download link
                    download_link = get_pdf_download_link(pdf_buffer, filename)
                    st.markdown(download_link, unsafe_allow_html=True)
                        
                    st.info("Click the link above to download your PDF report.")
                    
        st.markdown("</div>", unsafe_allow_html=True)

        # Horizontal line
        st.markdown("---")

        logger.info("App rendered successfully")

    except Exception as e:
        logger.error(f"An error occurred when rendering the UI components: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again.")


# === App Layout ===
def main():
    try:
        logger.debug("Starting Adaptive Traction Architecture Diagnostics app")

        # Initialize Session State
        init_session_state()

        # Load all the assets
        load_css("static/styles.css")
        load_js("static/script.js")

        # Add the toolbar
        add_toolbar()

        # Rendering UI components
        render_ui_components()

        # Add footer
        add_footer()

    except Exception as e:
        logger.error(f"An error occurred in the main app flow: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"Fatal error in app startup: {str(e)}", exc_info=True)
        st.error(f"Fatal error: {str(e)}")
