from django.conf import settings

from Emails.fakers.block import BlockTestFaker
from Emails.fakers.email import EmailTestFaker
from Emails.models import Block
from Emails.models import Email
from Emails.tests.abstract_test_classes import EmailsAbstractUtils


class TestEmailFakers(EmailsAbstractUtils):
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


class TestBlockFakers(EmailsAbstractUtils):
    def test_block_faker_creates_block(self):
        assert Block.objects.count() == 0
        block = BlockTestFaker()
        assert Block.objects.count() == 1
        assert block.title == 'test'
        assert block.content == 'test'
        assert block.show_link == True
        assert block.link_text == 'test'
        assert block.link == 'test.com'