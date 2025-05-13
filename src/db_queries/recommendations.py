import logging

from src.db_queries.connection import get_db_connection
import streamlit as st

logger = logging.getLogger(__name__)


@st.cache_data(ttl=3600)
def get_recommendations():
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT metric_id, recommendation
                           FROM recommendations
                           """)
            # Build a dictionary: {metric_id: [recommendation, ...], ...}
            recommendations_dict = {}
            for row in cursor.fetchall():
                metric_id = row['metric_id']
                rec = row['recommendation']
                if metric_id not in recommendations_dict:
                    recommendations_dict[metric_id] = []
                recommendations_dict[metric_id].append(rec)
            return recommendations_dict
    finally:
        pass


def get_recommendations_for_metric(metric_id):
    logger.debug(f"Get recommendations for metric {metric_id}")
    recs = get_recommendations()
    logger.debug(f"Debug - Metric {metric_id} has {len(recs.get(metric_id, []))} recs")
    return recs.get(metric_id, [])
