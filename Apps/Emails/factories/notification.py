from datetime import datetime

from django.db.models import Model
from django.utils.timezone import now
from django.utils.timezone import timedelta
from factory import post_generation
from factory.django import DjangoModelFactory

from Emails.factories.block import BlockFactory
from Emails.models import Notification


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model: Model = Notification

    is_test: bool = False
    programed_send_date: datetime = now() + timedelta(minutes=10)
    sent_date: datetime = None
    was_sent: bool = False

    @post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        if extracted:
            for block in extracted:
                self.blocks.add(block)
        else:
            self.blocks.add(BlockFactory())
