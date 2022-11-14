from datetime import datetime

from django.db.models import Model
from factory import SubFactory
from factory import post_generation
from factory.fuzzy import FuzzyChoice

from Emails.factories.email import EmailFactory
from Emails.fakers.block import BlockFaker
from Users.fakers.user import UserFaker
from Users.models import User


class EmailTestFaker(EmailFactory):
    subject: str = "Test subject"
    header: str = "Test header"
    is_test: bool = True
    to: User = SubFactory(UserFaker)
    programed_send_date: datetime = None
    sent_date: datetime = None
    affair: str = FuzzyChoice(
        (
            "NOTIFICATION",
            "PROMOTION",
            "GENERAL",
            "SETTINGS",
            "INVOICE",
            "SUGGESTION",
        )
    )

    @post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        self.blocks.add(BlockFaker())
