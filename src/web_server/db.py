import psycopg2

from web_server import utils
import json

conn_string = "host='localhost' dbname='web_server' user='postgres' password='postgres'"


def get_cursor():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    conn.autocommit = True
    return cursor


def get_users():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


def truncate_users():
    cursor = get_cursor()
    cursor.execute("TRUNCATE TABLE users")


def create_user(username, password):
    cursor = get_cursor()

    password, salt = utils.get_hash_with_salt(password)

    query = "INSERT INTO users(username, password, salt) VALUES (%s, %s, %s) RETURNING id;"
    cursor.execute(query, (username, password, salt))
    return cursor.fetchone()[0]


def get_valid_user(username, password):
    user_information = get_user_by_username(username)

    if not user_information:
        return False

    user_id, _, user_password, salt = user_information
    if user_password == utils.get_hash(password + salt):
        return user_id
    else:
        return False


def get_user_by_username(username):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", [username])
    return cursor.fetchone()


def get_user_by_user_id(user_id):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
    return cursor.fetchone()


def set_session_data(sessionid, data):
    cursor = get_cursor()
    data = json.dumps(data)
    query = "INSERT INTO sessions(sessionid, data) VALUES (%s, %s);"
    cursor.execute(query, (sessionid, data))
    return


def get_data_by_sessionid(sessionid):
    if sessionid:
        cursor = get_cursor()
        cursor.execute("SELECT data FROM sessions WHERE sessionid = %s", [sessionid])
        raw_data = cursor.fetchone()[0]
    else:
        raw_data = json.dumps('')
    return json.loads(raw_data)

def get_valid_sessionid(sessionid):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM sessions WHERE sessionid = %s", [sessionid])
    return cursor.fetchone()


def del_session(sessionid):
    cursor = get_cursor()
    cursor.execute("DELETE FROM sessions WHERE sessionid = %s", [sessionid])
    return


def get_all_users():
    cursor = get_cursor()
    cursor.execute("SELECT id, username FROM users")
    return cursor.fetchall()





def set_message(user_id, recipient_id, text_message):
    cursor = get_cursor()
    query = "INSERT INTO user_message (user_id, recipient_id, text_message) VALUES (%s, %s, %s);"
    cursor.execute(query, (user_id, recipient_id, text_message))
    return


def get_messages(user_id, recipient_id):
    cursor = get_cursor()
    query = """
        SELECT user_id, text_message
        FROM (
            SELECT *
            FROM user_message
            WHERE user_id=%s AND recipient_id=%s
            UNION
            SELECT *
            FROM user_message
            WHERE user_id=%s AND recipient_id=%s
        ) AS a
        ORDER BY created_at
    """
    cursor.execute(query, (user_id, recipient_id, recipient_id, user_id))
    return cursor.fetchall()


def check_id_in_db(user_id):
    if user_id:
        cursor = get_cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", [user_id])
        return cursor.fetchone()
    else:
        return None

