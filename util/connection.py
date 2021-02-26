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
    connection = connection or get_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()