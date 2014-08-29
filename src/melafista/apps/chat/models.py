from melafista import base_db


class Message:

    def __init__(self, user_id, recipient_id, text):
        self.user_id = user_id
        self.recipient_id = recipient_id
        self.text = text


    def create_message(self):
        query = "INSERT INTO users_message (user_id, recipient_id, text_message) VALUES (%s, %s, %s);"
        base_db.execute(query, self.user_id, self.recipient_id, self.text)

