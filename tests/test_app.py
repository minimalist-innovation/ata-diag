from streamlit.testing.v1 import AppTest
import pytest
from unittest.mock import patch
from app import initialize_session_state
from constants import REQUIRED_SESSION_KEYS


@pytest.fixture
def mock_session_state():
    with patch("streamlit.session_state", {}) as mock_state:
        yield mock_state


def test_initialize_session_state(mock_session_state):
    # Ensure session_state starts empty
    assert mock_session_state == {}
    initialize_session_state()

    expected_defaults = {
        'selected_saas_type': 'standard_saas',
        'selected_orientation': 'horizontal',
        'selected_industry': 'general_software',
        'annual_revenue': 1.0,
        'growth_stage_id': 0,
        'page_history': [],
        'current_page': None,
        'metrics_cache': {},
    }
    
    for key in REQUIRED_SESSION_KEYS:
        assert key in mock_session_state
        assert mock_session_state[key] == expected_defaults[key]


