import streamlit as st
from unittest.mock import patch
from src.components.global_assets import load_css, load_js
import streamlit.components.v1 as components

def test_load_css(tmp_path):
    """ We write a test that uses tmp_path (a built-in pytest fixture) to create a temporary CSS file"""
    """ Since streamlit.markdown causes a side effect (printing styled HTML in the Streamlit app), we will mock it in our tests."""
    css_content = """
    /* This is a comment */
    body {
        background-color: #f0f0f0;
        color: #333;
    }
    """
    css_file = tmp_path / "styles.css"
    css_file.write_text(css_content)

    expected_html = f"<style>{css_content}</style>"

    # Act & Assert
    with patch.object(st, "markdown") as mock_markdown:
        load_css(str(css_file))
        mock_markdown.assert_called_once_with(expected_html, unsafe_allow_html=True)


# Test for empty CSS file
def test_load_empty_css(tmp_path):
    css_file = tmp_path / "empty.css"
    css_file.write_text("")  # Create an empty file

    with patch.object(st, "markdown") as mock_markdown:
        load_css(str(css_file))
        mock_markdown.assert_called_once_with("<style></style>", unsafe_allow_html=True)


def test_load_js(tmp_path):
    """ Since components.html causes a side effect (printing styled HTML in the Streamlit app), we will mock it in our tests."""
    js_content = """
    // This is a test script
    function test() {
        alert("Hello");
    }
    """
    js_file = tmp_path / "script.js"
    js_file.write_text(js_content)

    expected_html = f"<script>{js_content}</script>"

    # Act & Assert
    with patch.object(components, "html") as mock_html:
        load_js(str(js_file))
        mock_html.assert_called_once_with(expected_html, height=0)


# Test for empty JS file
def test_load_empty_js(tmp_path):
    js_file = tmp_path / "empty.js"
    js_file.write_text("")  # Write empty content

    with patch.object(components, "html") as mock_html:
        load_js(str(js_file))
        mock_html.assert_called_once_with("<script></script>", height=0)




