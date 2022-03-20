from django.conf import settings
import factory

from Emails.models import Block


VERIFY_URL = f'{settings.URL}/api/v1/users'
RESET_PASSWORD_URL = f''  # Must redirect a front url with the token in url


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

    show_link = True
    content = settings.RESET_PASSWORD_EMAIL_CONTENT
    link_text = 'Reset password'
    link = factory.LazyAttribute(
        lambda object: f'{RESET_PASSWORD_URL}/' f'{object.instance.key}'
    )
    title = factory.LazyAttribute(
        lambda object: f'Hi, {object.instance.user.first_name}!'
    )


class VerifyEmailBlockFactory(BlockFactory):
    class Params:
        user = None

    title = factory.LazyAttribute(
        lambda object: f'Hi, {object.user.first_name}!'
    )
    link = factory.LazyAttribute(
        lambda object: (
            f'{VERIFY_URL}/{object.user.id}/verify/?token='
            f'{object.user.generate_verification_token()}'
        )
    )
    show_link = True
    content = settings.VERIFY_EMAIL_CONTENT
    link_text = 'Verify email'
