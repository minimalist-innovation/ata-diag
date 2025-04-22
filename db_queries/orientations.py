from db_queries.connection import get_db_connection


def get_orientations():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, orientation_name FROM orientations").fetchall()
    conn.close()
    return [dict(row) for row in rows]
