from mock import MagicMock
from mock import PropertyMock

from django.conf import settings

from Users.factories.user_factories import UserFactory
from Users.tests.abstract_test_classes import UsersAbstractUtils
from Emails.utils import get_email_data


class TestUserUtils(UsersAbstractUtils):
    def test_get_email_data_for_instance(self):
        instance = MagicMock()
        user = UserFactory()
        key = PropertyMock(return_value=10000)
        type(instance).key = key
        type(instance).user = user
        expected_data = {
            'greeting': f'Hi, {user.first_name}!',
            'link': 10000,
            'content': settings.RESET_PASSWORD_EMAIL_CONTENT,
        }
        actual_data = get_email_data('reset_password', instance)
        self.assertEqual(actual_data, expected_data)

    def test_get_email_data_for_user(self):
        user = UserFactory()
        expected_data = {
            'greeting': f'Hi, {user.first_name}!',
            'link': f'{settings.URL}/api/v1/users/{user.id}/verify/?token={user.generate_verification_token()}',
            'content': settings.VERIFY_EMAIL_CONTENT,
        }
        actual_data = get_email_data('verify_email', user)
        self.assertEqual(actual_data, expected_data)