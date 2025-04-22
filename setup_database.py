import sqlite3
import os
import logging
from streamlit import runtime
import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def execute_sql_file(conn, path):
    """Execute SQL file in proper order with transaction handling"""
    try:
        with open(path, 'r') as f:
            sql = f.read()
            conn.executescript(sql)
        logger.info(f"Executed SQL file: {os.path.basename(path)}")
    except Exception as e:
        logger.error(f"Error executing {path}: {str(e)}")
        raise


def setup_database(conn=None):
    """Main database setup orchestration"""
    try:
        logger.info("Starting database setup")
        # Check if the data directory exists, if not create it
        if not os.path.exists('data'):
            os.makedirs('data')
            logger.info("Created 'data' directory")

        if not conn:
            conn = sqlite3.connect('data/traction_diagnostics.db', check_same_thread=False)

        conn.execute("PRAGMA foreign_keys = ON")

        # Execution order matters!
        sql_files = [
            'sql_scripts/01_saas_types.sql',
            'sql_scripts/02_orientations.sql',
            'sql_scripts/03_industries.sql',
            'sql_scripts/04_growth_stages.sql',
            'sql_scripts/05_architecture_pillars.sql',
            'sql_scripts/06_metrics.sql',
            'sql_scripts/08_architecture_growth_stage_metric_associations.sql',
            'sql_scripts/07_industry_mappings.sql'
        ]

        # Execute all SQL files
        for sql_file in sql_files:
            execute_sql_file(conn, sql_file)

        conn.commit()
        logger.info("Database setup completed successfully")

        # Streamlit integration
        if runtime.exists():
            st.success("Database initialized successfully")

    except Exception as e:
        logger.error(f"Database setup failed: {str(e)}")
        if runtime.exists():
            st.error(f"Database error: {str(e)}")
        raise
    finally:
        if not conn:
            conn.close()


if __name__ == "__main__":
    setup_database()
