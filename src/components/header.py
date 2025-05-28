import base64
import os

import streamlit as st


def add_toolbar():
    # Create a placeholder for the toolbar
    toolbar_placeholder = st.empty()

    button_text = "Find Hidden Profit Leaks 🔍 [Claim Your Free Review]"
    if st.session_state.get("current_page", None) == "report_page.py":
        button_text = "Solve Hidden Profit Leaks → [Claim Your Fix Plan] 🔧"

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


def header():
    # All the logo
    add_logo(primary_color="#003580")

    # Add the toolbar
    add_toolbar()
