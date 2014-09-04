from django.shortcuts import redirect
from melafista import utils
from melafista.test_case import TestCase
from apps.users import models, auth
import mock


class TestAuthorizeUser(TestCase):
    @mock.patch('apps.users.auth._generate_sessionid')
    def test_success_authorize_user(self, mocked_generate_sessionid):
        sessioon_id = '123123'
        user_id = 123
        response = mock.MagicMock()

        mocked_generate_sessionid.return_value = sessioon_id

        auth.authorize_user(response, user_id)

        session = models.Session.objects.get(sessioon_id)
        self.assertEqual(session.data, {'user_id': user_id})

        response.set_cookie.assert_called_with(
            key=auth.SESSION_KEY,
            value=sessioon_id,
            max_age=None,
        )


class TestGetUserId(TestCase):
    def test_get_user_id(self):
        sessionid = '321'
        user_id = 123

        request = mock.MagicMock(
            COOKIES={auth.SESSION_KEY: sessionid}
        )
        models.Session.objects.create(sessionid, {'user_id': user_id})

        auth_user_id = auth.get_user_id(request)

        self.assertEqual(auth_user_id, user_id)

    def test_get_user_id_without_sessionid(self):
        sessionid = '321'
        user_id = 123

        request = mock.MagicMock(
            COOKIES={}
        )
        models.Session.objects.create(sessionid, {'user_id': user_id})
        auth_user_id = auth.get_user_id(request)

        self.assertEqual(auth_user_id, None)

    def test_get_user_id_wrong_sessionid(self):
        sessionid = '321'
        sessionid_in_db = '322'
        user_id = 123

        request = mock.MagicMock(
            COOKIES={auth.SESSION_KEY: sessionid}
        )
        models.Session.objects.create(sessionid_in_db, {'user_id': user_id})
        auth_user_id = auth.get_user_id(request)

        self.assertEqual(auth_user_id, None)


class TestLogoutUser(TestCase):
    def test_logout_user(self):
        session_id = '321'
        user_id = 123
        request = mock.MagicMock(COOKIES={auth.SESSION_KEY : session_id})
        models.Session.objects.create(session_id, {'user_id': user_id})
        response = mock.MagicMock()

        auth.logout_user(request, response)

        session = models.Session.objects.get(session_id)

        self.assertEqual(session, None)
        response.delete_cookie.assert_called_with(
            key=auth.SESSION_KEY
        )


class TestCheckAuthorization(TestCase):
    @mock.patch('apps.users.auth.get_user_id')
    def test_check_authorization(self, mocked_get_user_id):
        expected_response = mock.MagicMock()
        request = mock.MagicMock()

        real_func = mock.MagicMock(return_value=expected_response, __name__='real_func')
        func = auth.check_authorization(real_func)

        user_id = 123
        mocked_get_user_id.return_value = user_id

        actual_response = func(request)
        real_func.assert_called_with(request, user_id=user_id)
        self.assertIs(actual_response, expected_response)

    @mock.patch('apps.users.auth.get_user_id')
    def test_check_authorization_not_id(self, mocked_get_user_id):
        expected_response = redirect('/')

        real_func = mock.MagicMock(__name__='real_func')
        func = auth.check_authorization(real_func)

        mocked_get_user_id.return_value = None
        actual_response = func(None)

        self.assertEqual(actual_response.get('Location'), expected_response.get('Location'))
        self.assertEqual(real_func.call_count, 0)
        self.assertEqual(actual_response.status_code, 302)
