import json
from typing import Dict, List
from util.types import FieldValue
from util.connection import get_connection, fetch_sql

def data_for_item(item_id = None):
    connection = get_connection()
    with connection:
        jobs = jobs_producing(item_id, connection)
        for job in jobs:
            operations = fetch_job_operations(job["id"], connection)
            job["operations"] = operations
            state = json.loads(job.pop("state"))
            job["state"] = state[-1]["operation"]

    return jobs

def jobs_producing(item_id, connection):
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

    return fetch_sql(sql, connection)

def fetch_job_operations(job_id, connection):
    sql = "SELECT operations.id, operations.operation_type_id " \
          "FROM operations " \
          "JOIN job_associations " \
          "ON job_associations.operation_id = operations.id " \
          "WHERE job_associations.job_id = {job_id}".format(job_id = job_id)

    return fetch_sql(sql, connection)

def find_by_id(model, id):
    sql = "SELECT {model}s.* FROM {model}s " \
          "WHERE {model}s.id = {id} LIMIT 1".format(model = model, id = id)

    results = fetch_sql(sql)
    if results: return results[0]

def io_for(operation_id: int) -> List[FieldValue]:
    sql = "SELECT field_values.* FROM field_values " \
          "WHERE parent_class = 'Operation' " \
          "AND parent_id = '{operation_id}'".format(operation_id = operation_id)

    return fetch_sql(sql)

def data_associations_for(parent_class, parent_id):
    sql = "SELECT * FROM data_associations " \
          "WHERE parent_class = '{parent_class}' " \
          "AND parent_id = '{parent_id}'".format(parent_class = parent_class, parent_id = parent_id)

    return fetch_sql(sql)