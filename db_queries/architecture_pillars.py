from db_queries.connection import get_db_connection


def get_architecture_pillars():
    conn = get_db_connection()
    rows = conn.execute("""
                        SELECT id, pillar_name, description
                        FROM architecture_pillars
                        ORDER BY display_order
                        """).fetchall()
    conn.close()
    return [dict(row) for row in rows]
