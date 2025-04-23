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
    # Copyright footer with dynamically generated year
    current_year = datetime.now().year
    st.markdown(f"""
    <div class="footer">
        © {current_year} Minimalist Innovation LLC. All rights reserved.
    </div>
    """, unsafe_allow_html=True)


def add_toolbar():
    # st.markdown("""
    # <style>
    #     /* Hide Streamlit's default header and menu */
    #     header, #MainMenu, footer {visibility: hidden;}
    #
    #     /* Remove top margin/padding */
    #     .block-container { padding-top: 0 !important; margin-top: 0 !important; }
    #     .css-18e3th9 { padding-top: 0 !important; } /* Sometimes needed for newer Streamlit */
    # </style>
    # """, unsafe_allow_html=True)

    app_toolbar_html = f"""
        <div class="sticky-header">
            <div class="top-toolbar">
                <span class="toolbar-text">Need Clarity?</span>
                <a href="https://outlook.office.com/owa/calendar/MinimalistInnovationLLC@minimalistinnovation.onmicrosoft.com/bookings/s/H_o18Z1ej0OAvMiMMMyhTA2" 
                    class="toolbar-cta" 
                    target="_blank">
                    🤙 Schedule a Call Now
                </a>
            </div>
        </div>
    """
    st.markdown(app_toolbar_html, unsafe_allow_html=True)


# === Helper Functions ===
def add_logo(primary_color):
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
