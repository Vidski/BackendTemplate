from rest_framework.exceptions import PermissionDenied

from Users.factories.user_factories import UserFactory
from Users.tests.abstract_test_classes import UsersAbstractUtils
from Users.utils import verify_user_query_token


class TestUsertUtils(UsersAbstractUtils):

    def test_verify_user_query_token_raises_PermissionDenied(self):
        user = UserFactory()
        token =  "Wrong token"
        with self.assertRaises(PermissionDenied):
            verify_user_query_token(user, token)

    def test_verify_user_query_token_do_not_raise_anything(self):
        user = UserFactory()
        token =  user.generate_verification_token()
        verify_user_query_token(user, token)