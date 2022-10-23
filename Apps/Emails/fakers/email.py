from datetime import datetime

import factory
from django.db.models import Model

from Emails.factories.email import EmailFactory
from Emails.fakers.block import BlockFaker
from Users.factories.user import UserFactory
from Users.models import User


class EmailTestFaker(EmailFactory):
    subject: str = "Test subject"
    header: str = "Test header"
    is_test: bool = True
    to: User = factory.SubFactory(UserFactory)
    programed_send_date: datetime = None
    sent_date: datetime = None
    affair: str = factory.fuzzy.FuzzyChoice(
        (
            "NOTIFICATION",
            "PROMOTION",
            "GENERAL",
            "SETTINGS",
            "INVOICE",
            "SUGGESTION",
        )
    )

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        self.blocks.add(BlockFaker())
