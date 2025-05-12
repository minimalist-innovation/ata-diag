from db_queries.connection import get_db_connection


def determine_company_stage(revenue):
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, growth_stage_name, description FROM growth_stages WHERE ? BETWEEN low_range AND high_range',
                (revenue,)
            )
            # Create dictionary with ID as key and remaining columns as value
            growth_stages_dict = {
                row['id']: {
                    'growth_stage_name': row['growth_stage_name'],
                    'description': row['description']
                }
                for row in cursor.fetchall()
            }
            return growth_stages_dict
    finally:
        pass
