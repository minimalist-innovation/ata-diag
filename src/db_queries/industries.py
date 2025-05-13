# industries.py
from src.db_queries.connection import get_db_connection
import streamlit as st


@st.cache_data
def get_industry_mappings():
    """Load all industry mappings into memory"""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT saas_type_id, orientation_id, industry_id FROM industry_mappings')
            return [
                dict(row) for row in cursor.fetchall()
            ]
    finally:
        pass


@st.cache_data
def get_all_industries():
    """Load all industries into memory"""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, industry_name FROM industries')
            return {
                row['id']: dict(row) for row in cursor.fetchall()
            }
    finally:
        pass


def get_industries(saas_type_id=None, orientation_id=None):
    """In-memory filtering with optional parameters"""
    mappings = get_industry_mappings()
    industries = get_all_industries()

    matching_ids = [
        m['industry_id'] for m in mappings
        if (saas_type_id is None or m['saas_type_id'] == saas_type_id)
           and (orientation_id is None or m['orientation_id'] == orientation_id)
    ]

    return {
        iid: {'industry_name': industries[iid]['industry_name']}
        for iid in matching_ids
        if iid in industries
    }
