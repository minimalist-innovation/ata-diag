from db_queries.connection import get_db_connection


def get_saas_types():
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, type_name FROM saas_types")
            # Create dictionary with ID as key and remaining columns as value
            saas_types_dict = {
                row['id']: {
                    'type_name': row['type_name'],
                }
                for row in cursor.fetchall()
            }
            return saas_types_dict
    finally:
        pass
