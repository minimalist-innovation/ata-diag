from db_queries.connection import get_db_connection
from streamlit import cache_data


@cache_data(ttl=3600)  # Cache for 1 hour
def get_orientations():
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, orientation_name FROM orientations")
            # Create dictionary with ID as key and remaining columns as value
            orientations_dict = {
                row['id']: {
                    'orientation_name': row['orientation_name'],
                }
                for row in cursor.fetchall()
            }
            return orientations_dict
    finally:
        pass

