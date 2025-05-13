import time

import streamlit as st


def show_sequential_cta_toasts():
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

    # Add another small delay
    time.sleep(1)  # Allow final toast to display
