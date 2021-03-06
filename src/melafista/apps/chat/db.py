from melafista import base_db
from apps.chat import models

def create_message(user_id, recipient_id, text_message):
    cursor = base_db.get_cursor()
    query = "INSERT INTO users_message (user_id, recipient_id, text_message) VALUES (%s, %s, %s);"
    cursor.execute(query, (user_id, recipient_id, text_message))


def get_messages(user_id, recipient_id):
    query = """
        SELECT user_id, recipient_id, text_message
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
    fetched_data = base_db.fetchall(query, user_id, recipient_id, recipient_id, user_id)
    messages = []
    for i in fetched_data:
        messages.append(models.Message(*i))
    return messages


def get_number_new_messages(recipient_id):
    query = """SELECT user_id, COUNT(text_message) FROM users_message
                WHERE recipient_id=%s AND flag_reading=False  GROUP BY user_id"""
    number_messages = base_db.fetchall(query, recipient_id)

    return dict(number_messages)


def mark_messages_as_read(user_id, recipient_id):
    query = "UPDATE users_message  SET flag_reading = True WHERE recipient_id=%s AND user_id=%s "
    base_db.execute(query, user_id, recipient_id)
