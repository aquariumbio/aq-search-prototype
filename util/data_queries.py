from util.connection import get_connection, fetch_sql

def data_for_item(item_id = None):
    connection = get_connection()
    with connection:
        job_ids = jobs_producing(item_id)
        # job_items = fetch_job_items(connection)
        return job_ids

def jobs_producing(item_id):
    sql = "SELECT jbs.id FROM " \
              "(SELECT parent_id FROM field_values " \
              "WHERE parent_class = 'Operation' " \
              "AND role = 'input' " \
              "AND child_item_id = '{}') AS fvs " \
          "INNER JOIN operations AS ops " \
          "ON ops.id = fvs.parent_id " \
          "INNER JOIN job_associations AS jas " \
          "ON jas.operation_id = ops.id " \
          "INNER JOIN jobs AS jbs " \
          "ON jbs.id = jas.job_id " \
          "ORDER BY jbs.id".format(item_id)

    return fetch_sql(sql)

def fetch_job_items(connection):
    pass