
from web_server.db import get_cursor




def check_id_in_db(user_id):
    if user_id:
        cursor = get_cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", [user_id])
        return cursor.fetchone()
    else:
        return None

user_id = -21
a = check_id_in_db(user_id)

print a