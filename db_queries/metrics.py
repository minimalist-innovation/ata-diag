from db_queries.connection import get_db_connection


def get_metrics():
    conn = get_db_connection()
    rows = conn.execute("SELECT id,metric_name,description,blog_link,video_link,units FROM metrics").fetchall()
    conn.close()
    return [dict(row) for row in rows]
