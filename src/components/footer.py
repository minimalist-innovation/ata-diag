from datetime import datetime

import streamlit as st


def footer():
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
