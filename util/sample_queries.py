from util.connection import get_connection, fetch_sql

def search_sequential(terms, fields=[]):
    results = []
    connection = get_connection()
    with connection:
        for term in terms:
            results += select_samples(connection, term, fields=fields)
    return results

def all_samples(offset=0, limit=20):
    sql = "SELECT samples.*, sample_types.name, users.name " \
          "FROM samples " \
          "JOIN sample_types " \
          "ON sample_types.id = samples.sample_type_id " \
          "JOIN users " \
          "ON users.id = samples.user_id " \
          "ORDER BY samples.id LIMIT {}, {}".format(offset, limit)

    return fetch_sql(sql)

def count_samples():
    sql = "SELECT COUNT(*) FROM samples"

    return fetch_sql(sql)[0]['COUNT(*)']

def select_samples(connection, term, fields=[]):
    sql = "SELECT DISTINCT samples.*, sample_types.name, users.name " \
          "FROM samples " \
          "JOIN sample_types " \
          "ON sample_types.id = samples.sample_type_id " \
          "JOIN users " \
          "ON users.id = samples.user_id " \
          "JOIN field_values " \
          "ON field_values.parent_id = samples.id " \
          "WHERE field_values.parent_class = 'Sample' " \
          "AND CONCAT (" \
          "samples.name, samples.description"

    if "sample_type" in fields:
        sql += ", sample_types.name"
    if "owner" in fields:
        sql += ", users.name"
    if "properties" in fields:
        sql += ", field_values.name, field_values.value"

    sql += ") REGEXP '{}'".format(term)

    return fetch_sql(sql, connection)

def all_sample_properties(sample_ids):
    sql = "SELECT * FROM field_values " \
          "WHERE parent_class = 'Sample' " \
          "AND parent_id IN ({})".format(",".join(sample_ids))

    return fetch_sql(sql)
