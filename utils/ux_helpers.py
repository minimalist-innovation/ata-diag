import base64
import os
import time
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components


# Load CSS Dynamically
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load Javascript dynamically
def load_js(file_path):
    with open(file_path) as f:
        js_code = f.read()
        components.html(f"<script>{js_code}</script>", height=0)


def add_footer():
    """Responsive footer with hover-based disclaimer"""
    # Copyright footer with dynamically generated year
    current_year = datetime.now().year

    # Create a cleaner, more mobile-friendly footer
    st.markdown('<div class="content-wrapper"></div>', unsafe_allow_html=True)

    footer_html = f"""
    <div class="footer">
        <div class="footer-main">© {current_year} <a href="https://minimalistinnovation.com">Minimalist Innovation LLC</a>. All rights reserved.</div>
        <div class="footer-disclaimer">
            <span class="disclaimer-short">Use of this tool is at your own risk.</span>
            <span class="disclaimer-full">
                This tool is provided for informational and experimental purposes only and is
                provided 'as is' without warranties of any kind. Do not rely solely on the results for
                business decisions. Always consult with a qualified expert before taking action based
                on these diagnostics.
            </span>
        </div>
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)


def add_toolbar():
    # Create a placeholder for the toolbar
    toolbar_placeholder = st.empty()

    button_text = "🤙  Book Your FREE Startup Metrics Review Call"
    if st.session_state.get("diagnostics_run", True):
        button_text = "✅ Expert Analysis of Your Metrics - Book Your FREE Call"

    app_toolbar_html = f"""
        <div class="sticky-header">
            <div class="top-toolbar">
                <a href="https://outlook.office.com/owa/calendar/MinimalistInnovationLLC@minimalistinnovation.onmicrosoft.com/bookings/s/H_o18Z1ej0OAvMiMMMyhTA2" 
                    class="toolbar-cta" 
                    target="_blank">
                    <span class="cta-text">{button_text}</span>
                </a>
            </div>
            <div class="toolbar-spacer"></div>
        </div>
    """
    # Render the HTML in the placeholder
    clicked = toolbar_placeholder.html(app_toolbar_html)


def add_logo(primary_color):
    try:
        # Create a container with two columns - these will only be visible on desktop
        col1, col2 = st.columns([3, 1])

        # Get the absolute path to the logo
        logo_path = os.path.join("media", "Minimalist_Horizontal_Blue.svg")

        # Desktop view - both columns
        with col1:
            # Left side: App logo (will be hidden on mobile via CSS)
            app_logo_html = f"""
            <div class="app-logo-desktop-left">
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
            # Right side: Display company logo if exists (will be hidden on mobile via CSS)
            if os.path.exists(logo_path):
                with open(logo_path, "r") as f:
                    svg = f.read()
                    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
                    html = f"""
                        <div class="desktop-only-logo">
                            <img src="data:image/svg+xml;base64,{b64}"/>
                        </div>
                        """
                    st.markdown(html, unsafe_allow_html=True)
            else:
                st.write("")  # Empty space if logo doesn't exist

        # Mobile view - separate from columns, controlled by CSS media query
        # This will only be shown on mobile screens
        mobile_logo_html = f"""
        <div class="app-logo-mobile">
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
        st.markdown(mobile_logo_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error displaying logos: {str(e)}")


# ====== Stateful Slider======
def create_slider(metric, pillar_name, step_size, default_value, slider_format):
    slider_key = f"slider_{pillar_name}_{metric['id']}"

    return st.slider(
        label=f"{metric['metric_name']} ({metric['units']})",
        min_value=float(metric['min_value']),
        max_value=float(metric['max_value']),
        value=st.session_state.get(slider_key, default_value),
        step=step_size,
        format=slider_format,
        key=slider_key
    )


def show_sequential_toasts():
    # First toast - Explanation
    st.toast(
        "While your report is being generated, you can book a **FREE** strategy call to walk through your results and get a clear, **PERSONALIZED** plan.",
        icon="✨"
    )

    # Add a small delay between toasts
    time.sleep(.5)

    # Second toast - Direct to toolbar
    st.toast(
        "Click the **✅ Expert Analysis of Your Metrics - Book Your FREE Call** button in the top toolbar.",
        icon="👆"
    )

    # Add another small delay
    time.sleep(1)

    # Third toast - Reassurance
    st.toast(
        "30 minutes, no pressure - just clarity.",
        icon="👍"
    )


# Report Generation Helpers
def get_progress_column_config(units):
    """Return ProgressColumn config based on units"""
    config = {
        "label": "Current Value",
        "min_value": 0
    }

    if "Percentage" in units:
        config.update({
            "format": "%.1f%%",
            "max_value": 100
        })
    elif "Currency" in units:
        config.update({
            "format": "$%,.0f",
            "max_value": None  # Allow dynamic scaling
        })
    else:
        config.update({
            "format": "%.1f",
            "max_value": None
        })

    return st.column_config.ProgressColumn(**config)
