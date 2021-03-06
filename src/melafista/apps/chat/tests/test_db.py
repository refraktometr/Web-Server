from apps.chat import db as chat_db
from melafista.test_case import TestCase
from apps.users.tests import factories
# run test command string python manage.py test -v 2


class TestCreateMessage(TestCase):
    def test_success_create_message(self):
        user_id = factories.create_user()
        recipient_id = factories.create_user()
        text_message = 'Hello world'
        chat_db.create_message(user_id, recipient_id, text_message)

        fetched_query = chat_db.get_messages(user_id, recipient_id)

        self.assertEqual(text_message, fetched_query[0].text)
        self.assertEqual(user_id, fetched_query[0].user_id)


class TestGetMessage(TestCase):
    def test_success_get_messages(self):
        user_id = factories.create_user()
        recipient_id = factories.create_user()
        text_message = 'qwe'
        chat_db.create_message(user_id, recipient_id, text_message)

        messages = chat_db.get_messages(user_id, recipient_id)
        messages2 = chat_db.get_messages(recipient_id, user_id)

        self.assertEqual((user_id, text_message), (messages[0].user_id, messages[0].text))
        self.assertEqual((user_id, text_message), (messages2[0].user_id, messages2[0].text))

    def test_get_empty_messages(self):
        user_id = factories.create_user()
        recipient_id = factories.create_user()
        id_without_message = factories.create_user()
        text_message = 'Hello world'
        chat_db.create_message(user_id, recipient_id, text_message)

        fetched_data = chat_db.get_messages(id_without_message, user_id)
        fetched_data2 = chat_db.get_messages(recipient_id, id_without_message)

        self.assertEqual(fetched_data, [])
        self.assertEqual(fetched_data2, [])


class TestGetNumberNewMessages(TestCase):
    def test_get_number_new_messages(self):
        user_id = factories.create_user()
        user_id2 = factories.create_user()
        user_id3 = factories.create_user()
        text_message = 'Hello world'
        chat_db.create_message(user_id, user_id2, text_message)
        chat_db.create_message(user_id, user_id2, text_message)

        chat_db.create_message(user_id2, user_id, text_message)

        fetched_number_new_messages = chat_db.get_number_new_messages(user_id2)
        fetched_number = fetched_number_new_messages[user_id]

        self.assertEqual(2, fetched_number)


class TestMarkMessagesAsRead(TestCase):
    def test_mark_messages_as_read(self):
        user1 = factories.create_user()
        user2 = factories.create_user()
        user3 = factories.create_user()

        chat_db.create_message(user2, user1, 'Hello world')
        chat_db.create_message(user3, user1, 'Hello world')

        chat_db.mark_messages_as_read(user1, user2)

        fetched_data = chat_db.get_number_new_messages(user1)
        fetched_number = fetched_data.get(user2)
        fetched_number2 = fetched_data.get(user3)

        self.assertEqual(None, fetched_number)
        self.assertEqual(1, fetched_number2)
