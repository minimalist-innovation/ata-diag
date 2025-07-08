import os
import logging
import pytest
from unittest import mock
from unittest.mock import mock_open, patch

from src.utils.infra_helpers import setup_logging


@pytest.fixture
def mock_config_toml():
    return """
[logger]
level = "debug"
messageFormat = "%(levelname)s:%(message)s"
enableFileLogging = true
logFilePath = "test_logs/test.log"
"""


# when a valid config file exists
def test_logging_config_file_exists_and_valid(mock_config_toml, tmp_path):
    # Create a temporary .streamlit directory and config file
    config_dir = tmp_path / ".streamlit"
    config_dir.mkdir()
    config_file = config_dir / "config.toml"
    config_file.write_text(mock_config_toml)

    with patch("os.path.exists") as mock_exists, \
         patch("toml.load") as mock_toml_load, \
         patch("os.makedirs") as mock_makedirs, \
         patch("logging.FileHandler") as mock_file_handler:

        mock_exists.side_effect = lambda path: True if "config.toml" in path else False
        mock_toml_load.return_value = {
            "logger": {
                "level": "debug",
                "messageFormat": "%(levelname)s:%(message)s",
                "enableFileLogging": True,
                "logFilePath": "test_logs/test.log"
            }
        }

        result = setup_logging()

        assert result is True
        mock_file_handler.assert_called_once_with("test_logs/test.log")
