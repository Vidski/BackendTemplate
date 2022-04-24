import factory

from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.fakers.block import BlockTestFaker
from Users.factories.user import UserFactory


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
