from datetime import datetime

import factory
from django.db.models import Model

from Emails.factories.notification import NotificationFactory
from Emails.fakers.block import BlockFaker


class NotificationTestFaker(NotificationFactory):
    subject: str = "Test subject"
    header: str = "Test header"
    is_test: bool = True
    programed_send_date: datetime = None

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        self.blocks.add(BlockFaker())
