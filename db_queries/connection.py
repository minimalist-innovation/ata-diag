import os
import sqlite3
import logging
import streamlit as st


def get_db_connection():
    try:
        if not os.path.exists('data/traction_diagnostics.db'):
            from setup_database import setup_database
            setup_database()
        conn = sqlite3.connect('data/traction_diagnostics.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {str(e)}")
        st.error(f"Database connection error: {str(e)}")
        if 'conn' in locals() and conn:
            conn.close()
        st.stop()
