from melafista.test_case import TestCase
from apps.users.management import db as commands_db
from apps.users import db as user_db


class TestAuthorizeUser(TestCase):
    def test_authorize_user(self):

        authorize_user(response, user_id):