from django.conf import settings
import factory

from Emails.models import Block


class BlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Block

    title = factory.Faker('word')
    content = factory.Faker('sentence')
    show_link = factory.Faker('boolean')
    link_text = factory.Faker('word')
    link = factory.Faker('url')


class ResetPasswordBlockFactory(BlockFactory):
    class Params:
        instance = None

    title = factory.LazyAttribute(
        lambda object: (
            f'{settings.EMAIL_GREETING}' f' {object.instance.user.first_name}!'
        )
    )
    content = settings.RESET_PASSWORD_EMAIL_CONTENT
    show_link = True
    link_text = settings.RESET_PASSWORD_EMAIL_LINK_TEXT
    link = factory.LazyAttribute(
        lambda object: f'{settings.RESET_PASSWORD_URL}/{object.instance.key}'
    )


class VerifyEmailBlockFactory(BlockFactory):
    class Params:
        user = None

    title = factory.LazyAttribute(
        lambda object: (
            f'{settings.EMAIL_GREETING}' f'{object.user.first_name}!'
        )
    )
    content = settings.VERIFY_EMAIL_CONTENT
    show_link = True
    link_text = settings.VERIFY_EMAIL_LINK_TEXT
    link = factory.LazyAttribute(
        lambda object: (
            f'{settings.VERIFY_EMAIL_URL}/{object.user.id}/verify/?token='
            f'{object.user.generate_verification_token()}'
        )
    )


class SuggestionBlockFactory(BlockFactory):
    show_link = False
    link_text = ''
    link = ''
