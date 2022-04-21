import factory

from Emails.factories.email import EmailFactory
from Emails.factories.email import SuggestionEmailFactory
from Emails.fakers.block import BlockTestFaker
from Users.factories.user import UserFactory


class EmailTestFaker(EmailFactory):
    subject = 'Test subject'
    header = 'Test header'
    is_test = True
    to_all_users = False
    to = None
    programed_send_date = None
    sent_date = None
    was_sent = False

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        self.blocks.add(BlockTestFaker())


class SuggestionErrorFaker(SuggestionEmailFactory):
    subject = 'Test subject'
    header = 'Test header'
    sent_date = None
    was_sent = False
    was_read = False
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        self.blocks.add(BlockTestFaker())
