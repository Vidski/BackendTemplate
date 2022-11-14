from pytest import mark
from pytest import raises
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from Users.fakers.user import UserFaker
from Users.models import User
from Users.utils import check_e164_format
from Users.utils import generate_user_verification_token
from Users.utils import verify_user_query_token


@mark.django_db
class TestUserUtils:
    def test_verify_user_query_token_raises_PermissionDenied(self) -> None:
        user: User = UserFaker()
        token: str = "Wrong token"
        with raises(PermissionDenied):
            verify_user_query_token(user, token)

    def test_generate_user_verification_token_function(self) -> None:
        user: User = UserFaker()
        token: str = generate_user_verification_token(user)
        assert type(token) == str
        assert len(token) > 10

    def test_verify_user_query_token_do_not_raise_anything(self) -> None:
        user: User = UserFaker()
        token: str = generate_user_verification_token(user)
        verify_user_query_token(user, token)

    def test_check_e164_format_raises_PermissionDenied(self) -> None:
        phone_number: str = "000000000"
        with raises(ValidationError):
            check_e164_format(phone_number)

    def test_check_e164_format_do_not_raises_PermissionDenied(self) -> None:
        phone_number: str = "+00000000000"
        check_e164_format(phone_number)
