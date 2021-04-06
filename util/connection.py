import pymysql


def get_connection():
    return pymysql.connect(
        host='mysql_db',
        user='aquarium',
        password='aSecretAquarium',
        database='production',
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_sql(sql, connection=None):
    print(sql + "\n")
    data = None
    close = False
    if connection is None:
        connection =  get_connection()
        close = True

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()

    if close: connection.close()
    return data