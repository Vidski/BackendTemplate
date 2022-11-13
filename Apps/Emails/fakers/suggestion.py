from datetime import datetime

import factory
from django.db.models import Model
from factory import SubFactory
from factory import post_generation

from Emails.choices import CommentType
from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.fakers.block import BlockFaker
from Users.fakers.user import UserFaker


class SuggestionErrorFaker(SuggestionEmailFactory):
    subject: str = CommentType.SUGGESTION.value
    header: str = "Test header"
    sent_date: datetime = None
    was_sent: bool = False
    was_read: bool = False
    user = SubFactory(UserFaker)

    @post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        self.blocks.add(BlockFaker())
