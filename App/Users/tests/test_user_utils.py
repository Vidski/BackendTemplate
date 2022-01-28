from mock import MagicMock
from mock import PropertyMock
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied

from Users.factories.user_factories import UserFactory
from Users.tests.abstract_test_classes import UsersAbstractUtils
from Users.utils import get_email_data
from Users.utils import get_user_or_error
from Users.utils import verify_user_query_token


class TestUsertUtils(UsersAbstractUtils):

    def test_get_email_data_for_instance(self):
        instance = MagicMock()
        user = UserFactory()
        key = PropertyMock(return_value=10000)
        type(instance).key = key
        type(instance).user = user
        expected_data = {
            'name': user.first_name,
            'token': 10000
        }
        actual_data = get_email_data('reset_password', instance)
        self.assertEqual(actual_data, expected_data)

    def test_get_email_data_for_user(self):
        user = UserFactory()
        expected_data = {
            'id': user.id,
            'name': user.first_name,
            'token': user.generate_verification_token()
        }
        actual_data = get_email_data('verify_email', user)
        self.assertEqual(actual_data, expected_data)

    def test_get_user_or_error_raises_NotFound_when_users_not_exists(self):
        with self.assertRaises(NotFound):
            get_user_or_error(1, 2)

    def test_get_user_or_error_raises_PermissionDenied_looking_for_different_user(self):
        with self.assertRaises(PermissionDenied):
            get_user_or_error(self.normal_user, self.admin_user.id)

    def test_get_user_or_error_returns_different_user_looking_for_it_as_admin(self):
        instance = get_user_or_error(self.admin_user, self.normal_user.id)
        self.assertEqual(instance, self.normal_user)

    def test_get_user_or_error_raises_an_error_if_user_is_not_verified(self):
        with self.assertRaises(PermissionDenied):
            get_user_or_error(self.normal_user, self.normal_user.id)

    def test_get_user_or_error_returns_its_user(self):
        self.normal_user.verify()
        instance = get_user_or_error(self.normal_user, self.normal_user.id)
        self.assertEqual(instance, self.normal_user)

    def test_verify_user_query_token_raises_PermissionDenied(self):
        user = UserFactory()
        token =  "Wrong token"
        with self.assertRaises(PermissionDenied):
            verify_user_query_token(user, token)

    def test_verify_user_query_token_do_not_raise_anything(self):
        user = UserFactory()
        token =  user.generate_verification_token()
        verify_user_query_token(user, token)