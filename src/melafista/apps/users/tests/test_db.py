import json
from apps.users import db as user_db
from melafista import utils, base_db
from melafista.test_case import TestCase
from apps.users.tests import factories
from apps.users.management import db as management_db
# run test command string python manage.py test -v 2


class TestCreateUser(TestCase):
    def test_success_create(self):
        username = 'johndoe'
        password = '123123'

        user_id = user_db.create_user(username, password)

        fetched_user_id, fetched_username, fetched_password, salt = base_db.fetchone("SELECT * FROM users")

        self.assertIsInstance(fetched_user_id, int)
        self.assertEqual(user_id, fetched_user_id)
        self.assertEqual(username, fetched_username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=salt)
        self.assertEqual(hash_password, fetched_password)

    def test_returns_user_id(self):
        username = 'johndoe'
        password = '123123'

        user_id = user_db.create_user(username, password)
        self.assertIsInstance(user_id, int)

        _, fetched_username, _, _ = base_db.fetchone("SELECT * FROM users WHERE id=%s", user_id)

        self.assertEqual(username, fetched_username)

class TestGetValidUser(TestCase):
    def test_get_valid_user_return_user_id(self):
        username = 'johndoe'
        password = '123123'

        user_db.create_user(username, password)
        user_id = user_db.get_valid_user(username, password)

        self.assertIsInstance(user_id, int)

    def test_false_get_valid_user_wrong_username(self):
        username = 'johndoe'
        password = '123123'

        user_db.create_user(username, password)
        user_id = user_db.get_valid_user('False', password)

        self.assertEqual(user_id, None)

    def test_false_get_valid_user_wrong_password(self):
        username = 'johndoe'
        password = '123123'

        user_db.create_user(username, password)
        user_id = user_db.get_valid_user(username, 'false')

        self.assertEqual(user_id, None)


class TestGetUserByUsername(TestCase):
    def test_success_get_user_by_username(self):
        username = 'johndoe'
        password = '123123'
        user_db.create_user(username, password)

        fetched_id, fetched_username, fetched_password, fetched_salt = user_db.get_user_by_username(username)

        self.assertIsInstance(fetched_id, int)
        self.assertEqual(fetched_username, username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=fetched_salt)
        self.assertEqual(hash_password, fetched_password)


class TestGetUserByUserId(TestCase):
    def test_get_user_by_user_id(self):
        username = 'johndoe'
        password = '123123'
        user_db.create_user(username, password)

        user_id, _, _, _ = user_db.get_user_by_username(username)
        fetched_id, fetched_username, fetched_password, fetched_salt = user_db.get_user_by_user_id(user_id)


        self.assertIsInstance(fetched_id, int)
        self.assertEqual(user_id, fetched_id)
        self.assertEqual(fetched_username, username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=fetched_salt)
        self.assertEqual(hash_password, fetched_password)

class TestSetSessionData(TestCase):
    def test_set_session_data(self):
        username = 'johndoe'
        password = '123123'
        user_id = user_db.create_user(username, password)
        session_id = str(utils._gen_salt(50))
        data = {'user_id' : user_id}

        user_db.set_session_data(session_id, data)

        fetched_session_id, fetched_data, fetched_create_at = user_db.get_session_data(session_id)

        self.assertEqual(fetched_session_id, session_id)
        self.assertEqual(json.loads(fetched_data), data)
        self.assertEqual(fetched_data, json.dumps(data))


class TestSetSessionData(TestCase):
    def test_del_session(self):
        user_id1 = factories.create_user()
        user_id2 = factories.create_user()
        session_id = str(utils._gen_salt(50))
        session_id2 = str(utils._gen_salt(50))
        data = {'user_id' : user_id1}
        data2 = {'user_id' : user_id2}
        user_db.set_session_data(session_id, data)
        user_db.set_session_data(session_id2, data2)

        fetched_session_id, fetched_data, fetched_create_at = user_db.get_session_data(session_id)
        fetched_session_id2, fetched_data2, fetched_create_at2 = user_db.get_session_data(session_id2)

        self.assertEqual(fetched_session_id, session_id)
        self.assertEqual(json.loads(fetched_data), data)
        self.assertEqual(fetched_data, json.dumps(data))
        self.assertEqual(fetched_session_id2, session_id2)
        self.assertEqual(json.loads(fetched_data2), data2)


        user_db.del_session(session_id)

        deleted_row = user_db.get_session_data(session_id)
        self.assertEqual(deleted_row, None)
        self.assertEqual(fetched_session_id2, session_id2)
        self.assertEqual(json.loads(fetched_data2), data2)


class TestGetIdAndUsernameAllUsers(TestCase):
    def test_get_id_and_username_all_users(self):
        user1 = factories.create_user('vasia')
        user2 = factories.create_user('petiya')
        initial_array = [(user1, 'vasia'), (user2, 'petiya')]
        fetched_array = user_db.get_id_and_username_all_users()

        self.assertEqual(initial_array, fetched_array)
        self.assertEqual(len(fetched_array), 2)
