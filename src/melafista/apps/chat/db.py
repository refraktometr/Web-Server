from apps import users
from melafista import db as base_db

def set_message(user_id, recipient_id, text_message):
    cursor = base_db.get_cursor()
    query = "INSERT INTO users_message (user_id, recipient_id, text_message) VALUES (%s, %s, %s);"
    cursor.execute(query, (user_id, recipient_id, text_message))
    return


def get_messages(user_id, recipient_id):
    cursor = base_db.get_cursor()
    query = """
        SELECT user_id, text_message
        FROM (
            SELECT *
            FROM users_message
            WHERE user_id=%s AND recipient_id=%s
            UNION
            SELECT *
            FROM users_message
            WHERE user_id=%s AND recipient_id=%s
        ) AS a
        ORDER BY create_at
    """
    cursor.execute(query, (user_id, recipient_id, recipient_id, user_id))
    return cursor.fetchall()


def get_number_new_messages(recipient_id):
    cursor = base_db.get_cursor()
    query = """SELECT user_id, COUNT(text_message) FROM users_message
                WHERE recipient_id=%s AND flag_reading=False  GROUP BY user_id""" % recipient_id
    cursor.execute(query)
    number_messages = cursor.fetchall()

    return dict(number_messages)


def mark_messages_as_read(user_id, recipient_id):
    cursor = base_db.get_cursor()
    query = "UPDATE users_message  SET flag_reading = True WHERE recipient_id=%s AND user_id=%s "
    cursor.execute(query, (user_id, recipient_id))

