from datetime import datetime

import factory
import factory.fuzzy
from django.conf import settings
from django.db.models import Model
from django.utils import timezone
from django_rest_passwordreset.models import ResetPasswordToken

from Emails.factories.block import BlockFactory
from Emails.factories.block import ResetPasswordBlockFactory
from Emails.factories.block import VerifyEmailBlockFactory
from Emails.models import Block
from Emails.models import Email
from Project.utils.translation import get_translation_in
from Users.models import User


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = Email

    programed_send_date: datetime = timezone.now() + timezone.timedelta(
        minutes=10
    )
    was_sent: bool = False

    @factory.post_generation
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

    subject: str = factory.LazyAttribute(
        lambda object: get_translation_in(
            object.instance.user.preferred_language,
            settings.RESET_PASSWORD_EMAIL_SUBJECT,
        )
    )
    header: str = factory.LazyAttribute(
        lambda object: get_translation_in(
            object.instance.user.preferred_language,
            settings.RESET_PASSWORD_EMAIL_HEADER,
        )
    )
    to: User = factory.LazyAttribute(lambda object: object.instance.user)
    programed_send_date: datetime = None
    language: str = factory.LazyAttribute(
        lambda object: object.instance.user.preferred_language
    )

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        token: ResetPasswordToken = ResetPasswordToken.objects.filter(
            user_id=self.to.id
        ).last()
        block: Block = ResetPasswordBlockFactory(instance=token)
        self.blocks.add(block)


class VerifyEmailFactory(EmailFactory):
    class Params:
        instance: User = None

    subject: str = factory.LazyAttribute(
        lambda object: get_translation_in(
            object.instance.preferred_language, settings.VERIFY_EMAIL_SUBJECT
        )
    )
    header: str = factory.LazyAttribute(
        lambda object: get_translation_in(
            object.instance.preferred_language, settings.VERIFY_EMAIL_HEADER
        )
        + settings.APP_NAME
    )
    to: User = factory.LazyAttribute(lambda object: object.instance)
    programed_send_date: datetime = None
    language: str = factory.LazyAttribute(
        lambda object: object.instance.preferred_language
    )

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        block: Block = VerifyEmailBlockFactory(user=self.to)
        self.blocks.add(block)
