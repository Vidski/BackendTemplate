import factory

from Emails.fakers.block import BlockTestFaker
from Emails.factories.email import EmailFactory


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
