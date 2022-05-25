import pytest

from Emails.models.models import Block
from Emails.models.models import Email
from Users.models import Profile
from Users.models import User


@pytest.fixture(scope='function', autouse=True)
def setUp(django_db_blocker):
    with django_db_blocker.unblock():
        Email.objects.all().delete()
        Block.objects.all().delete()
        User.objects.all().delete()
        Profile.objects.all().delete()
