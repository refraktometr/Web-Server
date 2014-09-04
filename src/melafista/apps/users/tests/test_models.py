from melafista.test_case import TestCase
from apps.users import models
from melafista import utils, base_db
from apps.users.tests import factories

class TestUserCheckPassword(TestCase):
    def test_user_check_password(self):
        username = 'johndoe'
        password = '123123'

        models.User.objects.create(username, password)
        user = models.User.objects.get(username=username)

        self.assertEqual(user.check_password(password), True)

    def test_false_user_check_password_wrong_password(self):
        username = 'johndoe'
        password = '123123'

        models.User.objects.create(username, password)
        user = models.User.objects.get(username=username)

        self.assertEqual(user.check_password("False"), False)


class TestSetSessionData(TestCase):
    def test_set_session_data(self):
        username = 'johndoe'
        password = '123123'
        user = models.User.objects.create(username, password)
        session_id = str(utils.get_random_string(50))
        data = {'user_id' : user.id}

        models.Session.objects.create(session_id, data)

        session = models.Session.objects.get(session_id)

        self.assertEqual(session.data, data)


class TestDelSession(TestCase):
    def test_del_session(self):
        user = factories.create_user()
        user2 = factories.create_user()
        session_id = str(utils.get_random_string(50))
        session_id2 = str(utils.get_random_string(50))
        data = {'user_id': user.id}
        data2 = {'user_id': user2.id}
        models.Session.objects.create(session_id, data)
        models.Session.objects.create(session_id2, data2)

        models.Session.objects.delete(session_id)

        deleted_row = models.Session.objects.get(session_id)
        session2 = models.Session.objects.get(session_id2)

        self.assertEqual(deleted_row, None)
        self.assertEqual(session2.data, data2)


class TestCreateUser(TestCase):
    def test_success_create(self):
        username = 'johndoe'
        password = '123123'

        user = models.User.objects.create(username, password)

        fetched_user_id, fetched_username, fetched_password, salt = base_db.fetchone("SELECT * FROM users")

        self.assertIsInstance(fetched_user_id, int)
        self.assertEqual(user.id, fetched_user_id)
        self.assertEqual(username, fetched_username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=salt)
        self.assertEqual(hash_password, fetched_password)

    def test_returns_user_id(self):
        username = 'johndoe'
        password = '123123'

        user = models.User.objects.create(username, password)
        self.assertIsInstance(user.id, int)

        _, fetched_username, _, _ = base_db.fetchone("SELECT * FROM users WHERE id=%s", user.id)

        self.assertEqual(username, fetched_username)


class TestGetUserByUsername(TestCase):
    def test_success_get_user_by_username(self):
        username = 'johndoe'
        password = '123123'
        models.User.objects.create(username, password)

        user = models.User.objects.get(username=username)

        self.assertIsInstance(user.id, int)
        self.assertEqual(user.username, username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=user.salt)
        self.assertEqual(hash_password, user.password)

    def test_get_non_existent_username_returns_none(self):
        username = 'johndoe'
        password = '123123'
        models.User.objects.create(username, password)
        fetched_data = models.User.objects.get(username='qwe')

        self.assertEqual(fetched_data, None)


class TestGetUserByUserId(TestCase):
    def test_get_user_by_user_id(self):
        username = 'johndoe'
        password = '123123'
        models.User.objects.create(username, password)

        user = models.User.objects.get(username=username)
        fetched_user = models.User.objects.get(user_id=user.id)

        self.assertIsInstance(fetched_user.id, int)
        self.assertEqual(user.id, fetched_user.id)
        self.assertEqual(fetched_user.username, username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=fetched_user.salt)
        self.assertEqual(hash_password, fetched_user.password)

    def test_get_non_existent_user_id_returns_none(self):
        username = 'johndoe'
        password = '123123'
        user = models.User.objects.create(username, password)
        fetched_data = user.objects.get(user_id=12324)

        self.assertEqual(fetched_data, None)


class TestGetIdAndUsernameAllUsers(TestCase):
    def test_get_id_and_username_all_users(self):
        user1 = factories.create_user('vasia')
        user2 = factories.create_user('petiya')

        fetched_array = models.User.objects.get_all_users()

        self.assertEqual((user1.id, user1.username, user1.password, user1.salt),
                        (fetched_array[0].id, fetched_array[0].username, fetched_array[0].password, fetched_array[0].salt))
        self.assertEqual((user2.id, user2.username, user2.password, user2.salt),
                        (fetched_array[1].id, fetched_array[1].username, fetched_array[1].password, fetched_array[1].salt))
        self.assertEqual(len(fetched_array), 2)
