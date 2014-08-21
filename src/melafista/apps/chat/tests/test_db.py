from apps.chat import db as chat_db
from melafista.test_case import TestCase
from apps.users.management import db as management_db
# run test command string python manage.py test -v 2


class TestSetMessage(TestCase):
    def test_success_set_message(self):
        number_users = 2
        username, password, users_id = management_db.create_random_users_in_table_users(number_users)
        user_id = users_id[0]
        recipient_id = users_id[1]
        text_message = 'Hello world'
        chat_db.set_message(user_id, recipient_id, text_message)

        fetched_query = chat_db.get_messages(user_id, recipient_id)
        fetched_user_id, fetched_text_message = fetched_query[0]

        self.assertEqual(text_message, fetched_text_message)
        self.assertEqual(user_id, fetched_user_id)

class TestGetMessage(TestCase):
    def test_success_get_messages(self):
        number_users = 3
        username, password, users_id = management_db.create_random_users_in_table_users(number_users)
        user_id = users_id[0]
        recipient_id = users_id[1]
        text_message = 'qwe'
        chat_db.set_message(user_id, recipient_id, text_message)

        fetched_data = chat_db.get_messages(user_id, recipient_id)
        fetched_data2 = chat_db.get_messages(recipient_id, user_id)

        self.assertEqual([(user_id, text_message)], fetched_data)
        self.assertEqual([(user_id, text_message)], fetched_data2)

    def test_false_get_messages(self):
        number_users = 3
        username, password, users_id = management_db.create_random_users_in_table_users(number_users)
        user_id = users_id[0]
        recipient_id = users_id[1]
        id_without_message = users_id[2]
        text_message = 'Hello world'
        chat_db.set_message(user_id, recipient_id, text_message)

        fetched_data = chat_db.get_messages(id_without_message, user_id)
        fetched_data2 = chat_db.get_messages(recipient_id, id_without_message)

        self.assertEqual(fetched_data, [])
        self.assertEqual(fetched_data2, [])

class TestGetNumberNewMessages(TestCase):
    def test_get_number_new_messages(self):
        number_users = 3
        username, password, users_id = management_db.create_random_users_in_table_users(number_users)
        user_id = users_id[0]
        recipient_id = users_id[1]
        text_message = 'Hello world'
        number_new_messages = 5
        for i in range(number_new_messages):
            chat_db.set_message(user_id, recipient_id, text_message)

        fetched_number_new_messeges = chat_db.get_number_new_messages(recipient_id)
        fetched_number = fetched_number_new_messeges[user_id]

        self.assertEqual(number_new_messages, fetched_number)

class TestMarkMessagesAsRead(TestCase):
    def test_mark_messages_as_read(self):
        number_users = 3
        username, password, users_id = management_db.create_random_users_in_table_users(number_users)
        user_id = users_id[0]
        recipient_id = users_id[1]
        recipient_id2 = users_id[2]
        text_message = 'Hello world'
        number_new_messages = 5

        chat_db.set_message(user_id, recipient_id, text_message)
        chat_db.set_message(user_id, recipient_id2, text_message)
        fetched_number_new_messages = chat_db.get_number_new_messages(recipient_id)
        fetched_number_new_messages2 = chat_db.get_number_new_messages(recipient_id2)
        fetched_number = fetched_number_new_messages[user_id]
        fetched_number2 = fetched_number_new_messages2[user_id]
        self.assertEqual(1, fetched_number)
        self.assertEqual(1, fetched_number2)

        chat_db.mark_messages_as_read(recipient_id, user_id)

        fetched_number_new_messages = chat_db.get_number_new_messages(recipient_id)
        fetched_number_new_messages2 = chat_db.get_number_new_messages(recipient_id2)
        fetched_number = fetched_number_new_messages.get(user_id)
        fetched_number2 = fetched_number_new_messages2.get(user_id)
        self.assertEqual(None, fetched_number)
        self.assertEqual(1, fetched_number2)
