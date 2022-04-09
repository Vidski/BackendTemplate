import pytest

from Users.factories.profile import ProfileFactory
from Users.factories.user import UserFactory
from Users.models import Profile
from Users.models import User


@pytest.fixture(scope='function', autouse=True)
def setUp(django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.all().delete()
        Profile.objects.all().delete()


@pytest.mark.django_db
class TestUserFactory:
    def test_user_factory(self):
        assert User.objects.count() == 0
        user = UserFactory()
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email is not None
        assert user.phone_number is not None
        assert user.password is not None
        assert user.check_password('password') is True
        assert user.is_admin is False
        assert user.is_verified is False
