from src.db_queries.connection import get_db_connection
import streamlit as st


@st.cache_data
def get_all_growth_stages():
    """Load all growth stages into memory"""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, growth_stage_name, description, low_range, high_range FROM growth_stages')
            return {
                row['id']: dict(row) for row in cursor.fetchall()
            }
    finally:
        pass


def determine_company_stage(revenue):
    """In-memory revenue comparison"""
    stages = get_all_growth_stages().values()
    return {
        stage['id']: {
            'growth_stage_name': stage['growth_stage_name'],
            'description': stage['description']
        }
        for stage in stages
        if stage['low_range'] <= revenue <= stage['high_range']
    }
