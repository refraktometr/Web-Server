from apps.users import db as user_db
from melafista import utils, base_db
from melafista.test_case import TestCase
from apps.users.tests import factories
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

class TestUserChekPassword(TestCase):
    def test_user_check_password(self):
        username = 'johndoe'
        password = '123123'

        user_db.create_user(username, password)
        user = user_db.get_user(username=username)

        self.assertEqual(user.check_password(password), True)

    def test_false_user_check_password_wrong_password(self):
        username = 'johndoe'
        password = '123123'

        user_db.create_user(username, password)
        user = user_db.get_user(username=username)

        self.assertEqual(user.check_password("False"), False)


class TestGetUserByUsername(TestCase):
    def test_success_get_user_by_username(self):
        username = 'johndoe'
        password = '123123'
        user_db.create_user(username, password)

        user = user_db.get_user(username=username)

        self.assertIsInstance(user.id, int)
        self.assertEqual(user.username, username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=user.salt)
        self.assertEqual(hash_password, user.password)

    def test_get_non_existent_username_returns_none(self):
        username = 'johndoe'
        password = '123123'
        user_db.create_user(username, password)
        fetched_data = user_db.get_user(username='qwe')

        self.assertEqual(fetched_data, None)


class TestGetUserByUserId(TestCase):
    def test_get_user_by_user_id(self):
        username = 'johndoe'
        password = '123123'
        user_db.create_user(username, password)

        user = user_db.get_user(username=username)
        print user.id
        fetched_user = user_db.get_user(user_id=user.id)
        print fetched_user.id

        self.assertIsInstance(fetched_user.id, int)
        self.assertEqual(user.id, fetched_user.id)
        self.assertEqual(fetched_user.username, username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=fetched_user.salt)
        self.assertEqual(hash_password, fetched_user.password)

    def test_get_non_existent_user_id_returns_none(self):
        username = 'johndoe'
        password = '123123'
        user_db.create_user(username, password)
        fetched_data = user_db.get_user(user_id=12324)

        self.assertEqual(fetched_data, None)


class TestSetSessionData(TestCase):
    def test_set_session_data(self):
        username = 'johndoe'
        password = '123123'
        user_id = user_db.create_user(username, password)
        session_id = str(utils.get_random_string(50))
        data = {'user_id' : user_id}

        user_db.create_session_data(session_id, data)

        session = user_db.get_session(session_id)

        self.assertEqual(session.data, data)


class TestDelSession(TestCase):
    def test_del_session(self):
        user_id1 = factories.create_user()
        user_id2 = factories.create_user()
        session_id = str(utils.get_random_string(50))
        session_id2 = str(utils.get_random_string(50))
        data = {'user_id': user_id1}
        data2 = {'user_id': user_id2}
        user_db.create_session_data(session_id, data)
        user_db.create_session_data(session_id2, data2)

        user_db.del_session(session_id)

        deleted_row = user_db.get_session(session_id)
        session2 = user_db.get_session(session_id2)

        self.assertEqual(deleted_row, None)
        self.assertEqual(session2.data, data2)


class TestGetIdAndUsernameAllUsers(TestCase):
    def test_get_id_and_username_all_users(self):
        user1 = factories.create_user('vasia')
        user2 = factories.create_user('petiya')
        initial_array = [(user1, 'vasia'), (user2, 'petiya')]
        fetched_array = user_db.get_id_and_username_all_users()

        self.assertEqual(initial_array, fetched_array)
        self.assertEqual(len(fetched_array), 2)
