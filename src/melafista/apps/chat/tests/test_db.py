from apps.chat import models
from melafista.test_case import TestCase
from apps.users.tests import factories
# run test command string python manage.py test -v 2


class TestCreateMessage(TestCase):
    def test_success_create_message(self):
        user = factories.create_user()
        recipient = factories.create_user()
        text_message = 'Hello world'
        models.Message.objects.create_message(user.id, recipient.id, text_message)

        fetched_query = models.Message.objects.get_messages(user.id, recipient.id)

        self.assertEqual(text_message, fetched_query[0].text)
        self.assertEqual(user.id, fetched_query[0].user_id)


class TestGetMessage(TestCase):
    def test_success_get_messages(self):
        user = factories.create_user()
        recipient = factories.create_user()
        text_message = 'qwe'
        models.Message.objects.create_message(user.id, recipient.id, text_message)

        messages = models.Message.objects.get_messages(user.id, recipient.id)
        messages2 = models.Message.objects.get_messages(recipient.id, user.id)

        self.assertEqual((user.id, text_message), (messages[0].user_id, messages[0].text))
        self.assertEqual((user.id, text_message), (messages2[0].user_id, messages2[0].text))

    def test_get_empty_messages(self):
        user = factories.create_user()
        recipient = factories.create_user()
        user_without_message = factories.create_user()
        text_message = 'Hello world'
        models.Message.objects.create_message(user.id, recipient.id, text_message)

        fetched_data = models.Message.objects.get_messages(user_without_message.id, user.id)
        fetched_data2 = models.Message.objects.get_messages(recipient.id, user_without_message.id)

        self.assertEqual(fetched_data, [])
        self.assertEqual(fetched_data2, [])


class TestGetNumberNewMessages(TestCase):
    def test_get_number_new_messages(self):
        user = factories.create_user()
        user2 = factories.create_user()
        text_message = 'Hello world'
        models.Message.objects.create_message(user.id, user2.id, text_message)
        models.Message.objects.create_message(user.id, user2.id, text_message)

        models.Message.objects.create_message(user2.id, user.id, text_message)

        fetched_number_new_messages = models.Message.objects.get_number_new_messages(user2.id)
        fetched_number = fetched_number_new_messages[user.id]

        self.assertEqual(2, fetched_number)


class TestMarkMessagesAsRead(TestCase):
    def test_mark_messages_as_read(self):
        user1 = factories.create_user()
        user2 = factories.create_user()
        user3 = factories.create_user()

        models.Message.objects.create_message(user2.id, user1.id, 'Hello world')
        models.Message.objects.create_message(user3.id, user1.id, 'Hello world')

        models.Message.objects.mark_messages_as_read(user1.id, user2.id)

        fetched_data = models.Message.objects.get_number_new_messages(user1.id)
        fetched_number = fetched_data.get(user2.id)
        fetched_number2 = fetched_data.get(user3.id)

        self.assertEqual(None, fetched_number)
        self.assertEqual(1, fetched_number2)
