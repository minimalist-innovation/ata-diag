# Load CSS Dynamically
import streamlit as st
import streamlit.components.v1 as components


@st.cache_resource
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache_resource
def load_js(file_path):
    with open(file_path) as f:
        js_code = f.read()
        components.html(f"<script>{js_code}</script>", height=0)


def load_global_assets():
    # Load all the assets
    load_css("src/static/styles.css")
    load_js("src/static/script.js")
