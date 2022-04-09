import pytest

from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import Profile
from Users.models import User


@pytest.fixture(scope='function', autouse=True)
def setUp(django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.all().delete()
        Profile.objects.all().delete()


@pytest.mark.django_db
class TestUserFakers:
    def test_user_faker(self):
        assert User.objects.count() == 0
        user = UserFaker()
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == 'normaluser@appname.me'
        assert user.phone_number is not '+1123123123'
        assert user.password is not None
        assert user.check_password('password') is True
        assert user.is_admin is False
        assert user.is_verified is False

    def test_verified_user_faker(self):
        assert User.objects.count() == 0
        user = VerifiedUserFaker()
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == 'normaluser@appname.me'
        assert user.phone_number is not '+1123123123'
        assert user.password is not None
        assert user.check_password('password') is True
        assert user.is_admin is False
        assert user.is_verified is True

    def test_admin_user_faker(self):
        assert User.objects.count() == 0
        user = AdminFaker()
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == 'adminuser@appname.me'
        assert user.phone_number is not '+1123123124'
        assert user.password is not None
        assert user.check_password('password') is True
        assert user.is_admin is True
        assert user.is_verified is True
