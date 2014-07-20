import random
import psycopg2

conn_string = "host='localhost' dbname='test1' user='postgres' password='postgres'"


def get_cursor():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    conn.autocommit = True
    return cursor


def get_users():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


def create_user(username, password):
    cursor = get_cursor()
    salt = random.randint(0, 999999)
    query = "INSERT INTO users(username, password, salt) VALUES (%s, %s, %s) RETURNING id;"
    cursor.execute(query, (username, password, salt))
    return cursor.fetchone()[0]


def truncate_users():
    cursor = get_cursor()
    cursor.execute("TRUNCATE TABLE users")


def get_user_by_username(username):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", [username])
    return cursor.fetchone()


def get_user_by_user_id(user_id):
     cursor = get_cursor()
     cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
     return cursor.fetchone()
