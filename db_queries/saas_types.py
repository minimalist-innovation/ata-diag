from db_queries.connection import get_db_connection


def get_saas_types():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, type_name FROM saas_types").fetchall()
    conn.close()
    return [dict(row) for row in rows]
