from db_queries.connection import get_db_connection


def get_industries(saas_type_id, orientation_id):
    conn = get_db_connection()
    rows = conn.execute(
        '''
        SELECT i.id, i.industry_name
        FROM industry_mappings im
                 JOIN industries i ON im.industry_id = i.id
        WHERE im.saas_type_id = ?
          AND im.orientation_id = ?
        ''', (saas_type_id, orientation_id)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
