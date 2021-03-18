from util.connection import get_connection, fetch_sql

def data_for_item(item_id = None):
    connection = get_connection()
    with connection:
        jobs = jobs_producing(item_id)
        for job in jobs:
            operations = fetch_job_operations(job["id"])
            job["operation_ids"] = [op["id"] for op in operations]
        return jobs

def jobs_producing(item_id):
    sql = "SELECT jbs.id, jbs.state, fvs.name AS output_name FROM " \
              "(SELECT parent_id, name FROM field_values " \
              "WHERE parent_class = 'Operation' " \
              "AND role = 'output' " \
              "AND child_item_id = '{item_id}') AS fvs " \
          "INNER JOIN operations AS ops " \
          "ON ops.id = fvs.parent_id " \
          "INNER JOIN job_associations AS jas " \
          "ON jas.operation_id = ops.id " \
          "INNER JOIN jobs AS jbs " \
          "ON jbs.id = jas.job_id " \
          "ORDER BY jbs.id".format(item_id = item_id)

    return fetch_sql(sql)

def fetch_job_operations(job_id):
    sql = "SELECT operations.id " \
          "FROM operations " \
          "JOIN job_associations " \
          "ON job_associations.operation_id = operations.id " \
          "WHERE job_associations.job_id = {job_id}".format(job_id = job_id)

    return fetch_sql(sql)