from db_queries.connection import get_db_connection
import sqlite3


def get_all_metrics():
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT "
                           "id,"
                           "metric_name,"
                           "metric_type_id,"
                           "description,"
                           "blog_link,"
                           "video_link,"
                           "units FROM metrics").fetchall()
            metrics_dict = {
                row['id']: {
                    'metric_name': row['metric_name'],
                    'metric_type_id': row['metric_type_id'],
                    'description': row['description'],
                    'blog_link': row['blog_link'],
                    'video_link': row['video_link'],
                    'units': row['units']
                }
                for row in cursor.fetchall()
            }
            return metrics_dict
    finally:
        pass


def get_metrics(growth_stage_id, architecture_pillar_id, saas_type_id=None, industry_id=None):
    """Retrieve metrics with their value ranges based on growth stage, architecture pillar, and optional filters.

        Args:
            growth_stage_id (int): ID from growth_stages table
            architecture_pillar_id (int): ID from architecture_pillars table
            saas_type_id (int, optional): ID from saas_types table
            industry_id (int, optional): ID from industries table

        Returns:
            List[dict]: Metric associations with details and value ranges
        """
    conn = get_db_connection()
    try:
        # Base query with required parameters
        query = """
                SELECT agsma.id,
                       m.metric_name,
                       m.description,
                       m.blog_link,
                       m.video_link,
                       m.units,
                       agsma.min_value,
                       agsma.max_value,
                       agsma.lo_range_value,
                       agsma.hi_range_value,
                       m.metric_type_id,
                       mt.type_name
                FROM architecture_growth_stage_metric_associations agsma
                         JOIN metrics m ON agsma.metric_id = m.id
                         JOIN metric_types mt ON m.metric_type_id = mt.id
                WHERE agsma.enabled = 1
                  AND agsma.growth_stage_id = ?
                  AND agsma.architecture_pillar_id = ?
                """
        params = [growth_stage_id, architecture_pillar_id]

        # Handle SaaS type filtering with NULL awareness
        if saas_type_id is not None:
            query += " AND (agsma.saas_type_id = ? OR agsma.saas_type_id IS NULL)"
            params.append(saas_type_id)

        # Handle industry filtering with NULL awareness
        if industry_id is not None:
            query += " AND (agsma.industry_id = ? OR agsma.industry_id IS NULL)"
            params.append(industry_id)

        # Execute query
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            metrics_dict = {
                row['id']: {
                    'metric_name': row['metric_name'],
                    'metric_type_id': row['metric_type_id'],
                    'metric_type_name': row['type_name'],
                    'description': row['description'],
                    'blog_link': row['blog_link'],
                    'video_link': row['video_link'],
                    'units': row['units'],
                    'min_value': row['min_value'],
                    'max_value': row['max_value'],
                    'lo_range_value': row['lo_range_value'],
                    'hi_range_value': row['hi_range_value'],
                }
                for row in cursor.fetchall()
            }
            return metrics_dict

    except sqlite3.Error as e:
        return []
    finally:
        pass
