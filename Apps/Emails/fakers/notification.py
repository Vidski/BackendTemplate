from datetime import datetime

from django.db.models import Model
from factory import post_generation

from Emails.factories.notification import NotificationFactory
from Emails.fakers.block import BlockFaker


class NotificationTestFaker(NotificationFactory):
    subject: str = "Test subject"
    header: str = "Test header"
    is_test: bool = True
    programed_send_date: datetime = None

    @post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        self.blocks.add(BlockFaker())
