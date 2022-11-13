import pytest

from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import User


@pytest.mark.django_db
class TestUserFakers:
    def test_user_faker(self) -> None:
        assert User.objects.count() == 0
        user: User = UserFaker(
            email="normaluser@appname.me", phone_number="+1123123123"
        )
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == "normaluser@appname.me"
        assert str(user.phone_number) == "+1123123123"
        assert user.password is not None
        assert user.check_password("password") is True
        assert user.is_admin is False
        assert user.is_verified is False

    def test_verified_user_faker(self) -> None:
        assert User.objects.count() == 0
        user: User = VerifiedUserFaker(email="normalverifieduser@appname.me")
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == "normalverifieduser@appname.me"
        assert str(user.phone_number)[0] == "+"
        assert user.password is not None
        assert user.check_password("password") is True
        assert user.is_admin is False
        assert user.is_verified is True

    def test_admin_user_faker(self) -> None:
        assert User.objects.count() == 0
        user: User = AdminFaker(
            email="adminuser@appname.me", phone_number="+1123123124"
        )
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == "adminuser@appname.me"
        assert str(user.phone_number) == "+1123123124"
        assert user.password is not None
        assert user.check_password("password") is True
        assert user.is_admin is True
        assert user.is_verified is True
