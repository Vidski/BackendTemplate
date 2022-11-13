from datetime import datetime

from django.conf import settings
from django.db.models import Model
from django.utils.timezone import now
from django.utils.timezone import timedelta
from django_rest_passwordreset.models import ResetPasswordToken
from factory import LazyAttribute
from factory import post_generation
from factory.django import DjangoModelFactory

from Emails.factories.block import BlockFactory
from Emails.factories.block import ResetPasswordBlockFactory
from Emails.factories.block import VerifyEmailBlockFactory
from Emails.models import Block
from Emails.models import Email
from Project.utils.translation import get_translation_in
from Users.models import User


class EmailFactory(DjangoModelFactory):
    class Meta:
        model: Model = Email

    programed_send_date: datetime = now() + timedelta(minutes=10)
    was_sent: bool = False

    @post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        if not create:
            return
        if extracted:
            for block in extracted:
                self.blocks.add(block)
        else:
            self.blocks.add(BlockFactory())


class ResetEmailFactory(EmailFactory):
    class Params:
        instance: ResetPasswordToken = None

    subject: str = LazyAttribute(
        lambda object: get_translation_in(
            object.instance.user.preferred_language,
            settings.RESET_PASSWORD_EMAIL_SUBJECT,
        )
    )
    header: str = LazyAttribute(
        lambda object: get_translation_in(
            object.instance.user.preferred_language,
            settings.RESET_PASSWORD_EMAIL_HEADER,
        )
    )
    to: User = LazyAttribute(lambda object: object.instance.user)
    programed_send_date: datetime = None
    language: str = LazyAttribute(
        lambda object: object.instance.user.preferred_language
    )

    @post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        token: ResetPasswordToken = ResetPasswordToken.objects.filter(
            user_id=self.to.id
        ).last()
        block: Block = ResetPasswordBlockFactory(instance=token)
        self.blocks.add(block)


class VerifyEmailFactory(EmailFactory):
    class Params:
        instance: User = None

    subject: str = LazyAttribute(
        lambda object: get_translation_in(
            object.instance.preferred_language, settings.VERIFY_EMAIL_SUBJECT
        )
    )
    header: str = LazyAttribute(
        lambda object: get_translation_in(
            object.instance.preferred_language, settings.VERIFY_EMAIL_HEADER
        )
        + settings.APP_NAME
    )
    to: User = LazyAttribute(lambda object: object.instance)
    programed_send_date: datetime = None
    language: str = LazyAttribute(
        lambda object: object.instance.preferred_language
    )

    @post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        block: Block = VerifyEmailBlockFactory(user=self.to)
        self.blocks.add(block)
