import pytest
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from Users.factories.user import UserFactory
from Users.utils import check_e164_format
from Users.utils import verify_user_query_token


@pytest.mark.django_db
class TestUserUtils:
    def test_verify_user_query_token_raises_PermissionDenied(self):
        user = UserFactory()
        token = 'Wrong token'
        with pytest.raises(PermissionDenied):
            verify_user_query_token(user, token)

    def test_verify_user_query_token_do_not_raise_anything(self):
        user = UserFactory()
        token = user.generate_verification_token()
        verify_user_query_token(user, token)

    def test_check_e164_format_raises_PermissionDenied(self):
        phone_number = '000000000'
        with pytest.raises(ValidationError):
            check_e164_format(phone_number)

    def test_check_e164_format_do_not_raises_PermissionDenied(self):
        phone_number = '+00000000000'
        check_e164_format(phone_number)
