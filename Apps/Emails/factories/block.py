from django.conf import settings
from django.db.models import Model
from factory import LazyAttribute
from factory.django import DjangoModelFactory

from Emails.models import Block
from Project.utils.translation import get_translation_in
from Users.models import User
from Users.utils import generate_user_verification_token


class BlockFactory(DjangoModelFactory):
    class Meta:
        model: Model = Block

    show_link: bool = False
    link_text: str = ""
    link: str = ""


class ResetPasswordBlockFactory(BlockFactory):
    class Params:
        instance: User = None

    title: str = LazyAttribute(
        lambda object: (
            get_translation_in(
                object.instance.user.preferred_language, settings.EMAIL_GREETING
            )
            + f"{object.instance.user.first_name}!"
        )
    )
    content: str = LazyAttribute(
        lambda object: get_translation_in(
            object.instance.user.preferred_language,
            settings.RESET_PASSWORD_EMAIL_CONTENT,
        )
    )
    show_link: bool = True
    link_text: str = LazyAttribute(
        lambda object: get_translation_in(
            object.instance.user.preferred_language,
            settings.RESET_PASSWORD_EMAIL_LINK_TEXT,
        )
    )
    link: str = LazyAttribute(
        lambda object: f"{settings.RESET_PASSWORD_URL}/{object.instance.key}"
    )


class VerifyEmailBlockFactory(BlockFactory):
    class Params:
        user: User = None

    title: str = LazyAttribute(
        lambda object: (
            get_translation_in(
                object.user.preferred_language, settings.EMAIL_GREETING
            )
            + f" {object.user.first_name}!"
        )
    )
    content: str = LazyAttribute(
        lambda object: get_translation_in(
            object.user.preferred_language, settings.VERIFY_EMAIL_CONTENT
        )
    )
    show_link: bool = True
    link_text: str = LazyAttribute(
        lambda object: get_translation_in(
            object.user.preferred_language, settings.VERIFY_EMAIL_LINK_TEXT
        )
    )
    link: str = LazyAttribute(
        lambda object: (
            f"{settings.VERIFY_EMAIL_URL}/{object.user.id}/verify/?token="
            f"{generate_user_verification_token(object.user)}"
        )
    )


class SuggestionBlockFactory(BlockFactory):
    show_link: bool = False
    link_text: str = ""
    link: str = ""
