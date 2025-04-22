from db_queries.connection import get_db_connection
from streamlit import cache_data


@cache_data(ttl=3600)  # Cache for 1 hour
def get_industries(saas_type_id, orientation_id):
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                '''
                SELECT i.id, i.industry_name
                FROM industry_mappings im
                         JOIN industries i ON im.industry_id = i.id
                WHERE im.saas_type_id = ?
                  AND im.orientation_id = ?
                ''', (saas_type_id, orientation_id)
            )
            # Create dictionary with ID as key and remaining columns as value
            industries_dict = {
                row['id']: {
                    'industry_name': row['industry_name'],
                }
                for row in cursor.fetchall()
            }
            return industries_dict
    finally:
        pass

