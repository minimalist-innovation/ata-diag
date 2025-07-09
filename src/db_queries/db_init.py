import logging
import os
import sqlite3

import streamlit as st
from streamlit import runtime

from src.utils.infra_helpers import setup_logging

config_loaded = setup_logging()
logger = logging.getLogger(__name__)


def execute_sql_file(conn, path):
    """Execute SQL file in proper order with transaction handling"""
    try:
        with open(path, 'r', encoding="utf-8") as f:
            sql = f.read()
        conn.executescript(sql)
        logger.info(f"Executed SQL file: {os.path.basename(path)}")
    except Exception as e:
        logger.error(f"Error executing {path}: {str(e)}")
        raise


def setup_database(conn=None):
    """Main database setup orchestration"""
    try:
        db_dir = 'data'
        db_path = os.path.join(db_dir, 'traction_diagnostics.db')

        # Ensure the data directory exists
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created directory: {db_dir}")

        logger.info("Checking database setup")

        # Check if database file exists and has the required table
        if os.path.exists(db_path):
            check_conn = sqlite3.connect(db_path)
            cursor = check_conn.cursor()
            cursor.execute("""
                           SELECT name
                           FROM sqlite_master
                           WHERE type = 'table'
                             AND name = 'growth_stages'
                           """)
            if cursor.fetchone():
                logger.info("Database already initialized")
                check_conn.close()
                return
            check_conn.close()

        # Proceed with initialization if not exists or incomplete
        logger.info("Starting fresh database setup")
        if not conn:
            conn = sqlite3.connect(db_path, check_same_thread=False)

        conn.execute("PRAGMA foreign_keys = ON")

        # Execution order matters!
        sql_files = [
            'src/sql_scripts/01_saas_types.sql',
            'src/sql_scripts/02_orientations.sql',
            'src/sql_scripts/03_industries.sql',
            'src/sql_scripts/04_growth_stages.sql',
            'src/sql_scripts/05_architecture_pillars.sql',
            'src/sql_scripts/06_metric_types.sql',
            'src/sql_scripts/07_metrics.sql',
            'src/sql_scripts/08_industry_mappings.sql',
            'src/sql_scripts/09_architecture_growth_stage_metric_associations.sql',
            'src/sql_scripts/10_recommendations.sql'
        ]

        for sql_file in sql_files:
            execute_sql_file(conn, sql_file)

        conn.commit()
        logger.info("Database setup completed successfully")

    except Exception as e:
        logger.error(f"Database setup failed: {str(e)}")
        if runtime.exists():
            st.error(f"Database error: {str(e)}")
        raise

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    setup_database()
