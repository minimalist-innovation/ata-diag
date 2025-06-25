import pytest
import sqlite3
from unittest import mock
from src.db_queries.db_init import setup_database, execute_sql_file
import streamlit as st


@mock.patch("src.db_queries.db_init.os.path.exists")
@mock.patch("src.db_queries.db_init.os.makedirs")
@mock.patch("src.db_queries.db_init.sqlite3.connect")
@mock.patch("src.db_queries.db_init.execute_sql_file")
@mock.patch("src.db_queries.db_init.logger")
@mock.patch("src.db_queries.db_init.st")
def test_setup_database_fresh_setup(
    mock_st, mock_logger, mock_execute_sql_file, mock_connect, mock_makedirs, mock_exists
):
    # Mock database file and directory checks
    def exists_side_effect(path):
        if 'traction_diagnostics.db' in path:
            return False
        elif 'data' in path:
            return False
        return True

    mock_exists.side_effect = exists_side_effect

    # Mock connection and cursor behavior
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_connect.return_value = mock_conn

    # Call the function
    setup_database()

    # Directory creation should be called
    mock_makedirs.assert_called_once_with("data")

    # Connection should be established
    mock_connect.assert_called()

    # SQL files should be executed
    assert mock_execute_sql_file.call_count == 10

    # Commit and close should be called
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

    # No Streamlit error should be triggered
    mock_st.error.assert_not_called()


# Database Already Initialized
@mock.patch("src.db_queries.db_init.os.path.exists")
@mock.patch("src.db_queries.db_init.sqlite3.connect")
@mock.patch("src.db_queries.db_init.logger")
@mock.patch("src.db_queries.db_init.st")
def test_setup_database_already_initialized(mock_st, mock_logger, mock_connect, mock_exists):
    """ This verifies that if the growth_stages table exists, the setup exits early."""
    # Simulate existing database and table
    def exists_side_effect(path):
        return True

    mock_exists.side_effect = exists_side_effect

    # Mock connection and cursor
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_cursor.fetchone.return_value = ('growth_stages',)
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    # Run function
    setup_database()

    # Should detect already initialized and exit early
    mock_cursor.execute.assert_called_once()
    mock_conn.close.assert_called_once()

    # No SQL execution or commit expected
    mock_connect.assert_called_once()
    mock_st.error.assert_not_called()


# Streamlit Error Display when runtime.exists() is True
@mock.patch("src.db_queries.db_init.os.path.exists")
@mock.patch("src.db_queries.db_init.os.makedirs")
@mock.patch("src.db_queries.db_init.sqlite3.connect")
@mock.patch("src.db_queries.db_init.execute_sql_file")
@mock.patch("src.db_queries.db_init.runtime.exists")
@mock.patch("src.db_queries.db_init.logger")
@mock.patch("src.db_queries.db_init.st")
def test_setup_database_streamlit_error_display(
    mock_st, mock_logger, mock_runtime_exists, mock_execute_sql_file,
    mock_connect, mock_makedirs, mock_exists
):
    """ test how the setup_database() function behaves when an SQL execution error occurs and Streamlit is available to show the error."""
    mock_exists.return_value = False
    mock_runtime_exists.return_value = True

    mock_conn = mock.Mock()
    mock_connect.return_value = mock_conn

    mock_execute_sql_file.side_effect = Exception("Critical SQL failure")

    with pytest.raises(Exception, match="Critical SQL failure"):
        setup_database()

    # Streamlit error should be shown
    mock_st.error.assert_called_once()
    mock_conn.close.assert_called_once()


# SQL File Execution Fails
@mock.patch("src.db_queries.db_init.os.path.exists")
@mock.patch("src.db_queries.db_init.os.makedirs")
@mock.patch("src.db_queries.db_init.sqlite3.connect")
@mock.patch("src.db_queries.db_init.execute_sql_file")
@mock.patch("src.db_queries.db_init.logger")
@mock.patch("src.db_queries.db_init.st")
def test_setup_database_sql_file_execution_error(
    mock_st, mock_logger, mock_execute_sql_file, mock_connect, mock_makedirs, mock_exists
):
    """ Simulates failure in one of the SQL script executions. """
    # Simulate fresh setup
    mock_exists.return_value = False
    mock_conn = mock.Mock()
    mock_connect.return_value = mock_conn

    # Simulate failure in SQL execution
    mock_execute_sql_file.side_effect = Exception("SQL error")

    with pytest.raises(Exception, match="SQL error"):
        setup_database()

    # Should attempt to make directory
    mock_makedirs.assert_called_once()

    # Streamlit error should not be triggered yet (runtime.exists() not simulated)
    mock_st.error.assert_not_called()
    mock_conn.close.assert_called_once()


# SQL file executes successfully
@mock.patch("src.db_queries.db_init.open", new_callable=mock.mock_open, read_data="CREATE TABLE test (id INTEGER);")
@mock.patch("src.db_queries.db_init.logger")
def test_execute_sql_file_success(mock_logger, mock_open):
    # Create a mock connection with executescript()
    mock_conn = mock.Mock()

    # Call the function
    execute_sql_file(mock_conn, "fake_path.sql")

    # Assert open() was called with correct path
    mock_open.assert_called_once_with("fake_path.sql", 'r')

    # Assert executescript() was called with the SQL content
    mock_conn.executescript.assert_called_once_with("CREATE TABLE test (id INTEGER);")

    # Assert logger.info was called
    mock_logger.info.assert_called_once()


# Test SQL Execution Raises an Error
@mock.patch("src.db_queries.db_init.open", new_callable=mock.mock_open, read_data="BAD SQL;")
@mock.patch("src.db_queries.db_init.logger")
def test_execute_sql_file_failure(mock_logger, mock_open):
    # Create a mock connection that raises an error
    mock_conn = mock.Mock()
    mock_conn.executescript.side_effect = Exception("SQL syntax error")

    # Run and assert exception is raised
    with pytest.raises(Exception, match="SQL syntax error"):
        execute_sql_file(mock_conn, "bad_path.sql")

    # Assert file was opened
    mock_open.assert_called_once_with("bad_path.sql", 'r')

    # Assert executescript was called
    mock_conn.executescript.assert_called_once()

    # Assert logger.error was called
    mock_logger.error.assert_called_once()




