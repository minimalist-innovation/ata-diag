from db_queries.connection import get_db_connection


def get_architecture_pillars():
    """Return architecture pillars as a dictionary with IDs as keys"""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT id, pillar_name, description, display_icon
                           FROM architecture_pillars
                           WHERE enabled = TRUE
                           ORDER BY display_order
                           """)

            # Create dictionary with ID as key and remaining columns as value
            pillars_dict = {
                row['id']: {
                    'pillar_name': row['pillar_name'],
                    'description': row['description'],
                    'display_icon': row['display_icon']
                }
                for row in cursor.fetchall()
            }
            return pillars_dict
    finally:
        pass
