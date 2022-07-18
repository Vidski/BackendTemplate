import factory
from datetime import datetime
from Emails.factories.email import EmailFactory
from Emails.fakers.block import BlockTestFaker
from Users.factories.user import UserFactory
from Users.models import User

from django.db.models import Model


class EmailTestFaker(EmailFactory):
    subject: str = "Test subject"
    header: str = "Test header"
    is_test: bool = True
    to: User = factory.SubFactory(UserFactory)
    programed_send_date: datetime = None
    sent_date: datetime = None
    was_sent: bool = False

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        self.blocks.add(BlockTestFaker())
