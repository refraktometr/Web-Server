from apps.users import db
from melafista import utils, db as base_db
from melafista.test_case import TestCase


class TestCreateUser(TestCase):
    def test_success_create(self):
        username = 'johndoe'
        password = '123123'

        db.create_user(username, password)

        user_id, fetched_username, fetched_password, salt = base_db.fetchone("SELECT * FROM users")

        self.assertIsInstance(user_id, int)
        self.assertEqual(username, fetched_username)

        hash_password, _ = utils.get_hash_with_salt(password, salt=salt)
        self.assertEqual(hash_password, fetched_password)

    def test_returns_user_id(self):
        username = 'johndoe'
        password = '123123'

        user_id = db.create_user(username, password)
        self.assertIsInstance(user_id, int)

        _, fetched_username, _, _ = base_db.fetchone("SELECT * FROM users WHERE id=%s", user_id)

        self.assertEqual(username, fetched_username)
