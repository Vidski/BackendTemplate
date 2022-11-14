from django.conf import settings
from django.db.models import Model
from factory import LazyAttribute
from factory import post_generation
from factory.django import DjangoModelFactory
from rest_framework.exceptions import ParseError

from Emails.choices import CommentType
from Emails.factories.block import SuggestionBlockFactory
from Emails.models import Block
from Emails.models import Suggestion


class SuggestionEmailFactory(DjangoModelFactory):
    class Meta:
        model: Model = Suggestion

    class Params:
        type: str = ""
        content: str = ""

    subject: str = LazyAttribute(
        lambda object: get_subject_for_suggestion(object.type, object.content)
    )

    @post_generation
    def header(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        self.header = (
            f'{self.subject.split("||")[0][:-1]}'
            + f" {settings.SUGGESTIONS_EMAIL_HEADER}"
            + f" {self.user.id}"
        )

    @post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        subject_splitted: list = self.subject.split("||")
        type: str = subject_splitted[0][:-1]
        content: str = subject_splitted[1][1:]
        self.subject: str = type
        self.save()
        block: Block = SuggestionBlockFactory(
            title=self.header,
            content=content,
            show_link=True,
            link_text=settings.SUGGESTIONS_EMAIL_LINK_TEXT,
            link=f"{settings.URL}/api/suggestions/{self.id}/read/",
        )
        self.blocks.add(block)


def get_subject_for_suggestion(suggestion_type: str, content: str) -> str:
    if suggestion_type not in CommentType.values:
        raise ParseError("Type not allowed")
    return f'{suggestion_type} || {content.replace("||", "")}'
