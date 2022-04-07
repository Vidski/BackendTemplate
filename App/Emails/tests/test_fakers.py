import pytest

from django.conf import settings

from Emails.fakers.block import BlockTestFaker
from Emails.fakers.email import EmailTestFaker
from Emails.models import Block
from Emails.models import Email
from Users.models import Profile
from Users.models import User


@pytest.fixture(scope="function", autouse=True)
def setUp(django_db_blocker):
    with django_db_blocker.unblock():
        Email.objects.all().delete()
        Block.objects.all().delete()
        User.objects.all().delete()
        Profile.objects.all().delete()


@pytest.mark.django_db
class TestEmailFakers:
    def test_email_faker_creates_email_with_block(self):
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        email = EmailTestFaker()
        assert Email.objects.count() == 1
        assert Block.objects.count() == 1
        assert email.subject == 'Test subject'
        assert email.header == 'Test header'
        assert email.is_test == True
        assert email.to == f'{settings.TEST_EMAIL}'
        assert email.to_all_users == False
        assert email.blocks.first() is not None
        block = email.blocks.first()
        assert block.title == 'test'
        assert block.content == 'test'
        assert block.show_link == True
        assert block.link_text == 'test'
        assert block.link == 'test.com'


@pytest.mark.django_db
class TestBlockFakers:
    def test_block_faker_creates_block(self):
        assert Block.objects.count() == 0
        block = BlockTestFaker()
        assert Block.objects.count() == 1
        assert block.title == 'test'
        assert block.content == 'test'
        assert block.show_link == True
        assert block.link_text == 'test'
        assert block.link == 'test.com'
