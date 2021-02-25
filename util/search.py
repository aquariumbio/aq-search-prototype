from util.connection import get_connection


def search_sequential(terms):
    results = []
    connection = get_connection()
    with connection:
        for term in terms:
            results += select_samples(connection, term)
    return results

def all_samples(offset=0, limit=20):
    sql = "SELECT samples.*, sample_types.name, users.name " \
          "FROM samples " \
          "JOIN sample_types " \
          "ON sample_types.id = samples.sample_type_id " \
          "JOIN users " \
          "ON users.id = samples.user_id " \
          "ORDER BY samples.id LIMIT {}, {}".format(offset, limit)

    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql)

    print(sql + "\n")
    return cursor.fetchall()

def count_samples():
    sql = "SELECT COUNT(*) FROM samples"

    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql)

    print(sql + "\n")
    return cursor.fetchone()['COUNT(*)']

def select_samples(connection, term):
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
          "sample_types.name, users.name, " \
          "samples.name, samples.description, " \
          "field_values.name, field_values.value" \
          ") REGEXP '{}'".format(term)

    with connection.cursor() as cursor:
        cursor.execute(sql)

    print(sql + "\n")
    return cursor.fetchall()

def all_sample_properties(sample_ids):
    sql = "SELECT * FROM field_values " \
          "WHERE parent_class = 'Sample' " \
          "AND parent_id IN ({})".format(",".join(sample_ids))

    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)

    print(sql + "\n")
    return cursor.fetchall()

def split(terms, sep=" "):
    return terms.split(sep)
