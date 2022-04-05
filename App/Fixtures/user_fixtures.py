import pytest

from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


@pytest.fixture(scope="function")
def admin(django_db_blocker):
    with django_db_blocker.unblock():
        admin = AdminFaker()
        yield admin
        admin.delete()


@pytest.fixture(scope="function")
def user(django_db_blocker):
    with django_db_blocker.unblock():
        user = UserFaker()
        yield user
        user.delete()


@pytest.fixture(scope="function", autouse=True)
def setUp(django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.all().delete()
