import os
import sqlite3
import logging
import streamlit as st
from streamlit import cache_resource


@cache_resource
def get_db_connection():
    """Cache database connection with proper lifecycle management"""
    try:
        # Ensure database exists before connecting
        if not os.path.exists('data/traction_diagnostics.db'):
            with sqlite3.connect('data/traction_diagnostics.db') as temp_conn:
                from setup_database import setup_database
                setup_database(temp_conn)

        # Main app connection
        conn = sqlite3.connect('data/traction_diagnostics.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {str(e)}")
        st.error(f"Database connection error: {str(e)}")
        st.stop()
