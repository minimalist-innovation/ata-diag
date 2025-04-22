from db_queries.connection import get_db_connection


def determine_company_stage(revenue):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT growth_stage_name, description FROM growth_stages WHERE ? BETWEEN low_range AND high_range',
            (revenue,)
        )
        result = cursor.fetchone()
        if result:
            return result['growth_stage_name'], result['description']
        else:
            return "Undetermined", "We couldn't determine your company stage. Please contact support."
    finally:
        conn.close()
