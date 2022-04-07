import pytest
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from Users.factories.user import UserFactory
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import Profile
from Users.models import User
from Users.utils import check_e164_format
from Users.utils import get_user_or_error
from Users.utils import verify_user_query_token


@pytest.fixture(scope="function", autouse=True)
def setUp(django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.all().delete()
        Profile.objects.all().delete()


@pytest.mark.django_db
class TestUserUtils:
    def test_get_user_or_error_raises_NotFound_when_users_not_exists(self):
        with pytest.raises(NotFound):
            get_user_or_error(1, 2)

    def test_get_user_or_error_raises_PermissionDenied_looking_for_different_user(
        self,
    ):
        admin = AdminFaker()
        user = UserFaker()
        with pytest.raises(PermissionDenied):
            get_user_or_error(user, admin.id)

    def test_get_user_or_error_returns_different_user_looking_for_it_as_admin(
        self,
    ):
        admin = AdminFaker()
        user = UserFaker()
        instance = get_user_or_error(admin, user.id)
        assert instance == user

    def test_get_user_or_error_raises_an_error_if_user_is_not_verified(self):
        user = UserFaker()
        with pytest.raises(PermissionDenied):
            get_user_or_error(user, user.id)

    def test_get_user_or_error_returns_its_user(self):
        user = VerifiedUserFaker()
        instance = get_user_or_error(user, user.id)
        assert instance == user

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
