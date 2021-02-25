import pymysql


def get_connection():
    return pymysql.connect(
        host='mysql_db',
        user='aquarium',
        password='aSecretAquarium',
        database='production',
        cursorclass=pymysql.cursors.DictCursor
    )