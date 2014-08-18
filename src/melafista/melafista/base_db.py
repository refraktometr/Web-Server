from django.conf import settings
import psycopg2


def get_cursor():
    conn = psycopg2.connect("host=localhost dbname=%(NAME)s user=%(USER)s password=%(PASSWORD)s" % settings.DATABASES['default'])
    cursor = conn.cursor()
    conn.autocommit = True
    return cursor


def fetchone(query, *params):
    cursor = get_cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchone()


def fetchall(query, *params):
    cursor = get_cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()
