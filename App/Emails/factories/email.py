import factory
from django.conf import settings
from django.utils import timezone
from django_rest_passwordreset.models import ResetPasswordToken

from Emails.factories.block import BlockFactory
from Emails.factories.block import ResetPasswordBlockFactory
from Emails.factories.block import VerifyEmailBlockFactory
from Emails.models import Email
from Users.models import User


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Email

    subject = factory.Faker('sentence')
    header = factory.Faker('word')
    is_test = False
    to_all_users = False
    to = factory.Faker('email')
    programed_send_date = factory.Faker(
        'date_time', tzinfo=timezone.get_current_timezone()
    )
    sent_date = factory.Faker(
        'date_time', tzinfo=timezone.get_current_timezone()
    )
    was_sent = False

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for block in extracted:
                self.blocks.add(block)
        else:
            self.blocks.add(BlockFactory())


class ResetEmailFactory(EmailFactory):
    class Params:
        instance = None

    subject = settings.RESET_PASSWORD_EMAIL_SUBJECT
    header = settings.RESET_PASSWORD_EMAIL_HEADER
    to = factory.LazyAttribute(lambda object: f'{object.instance.user.email}')
    programed_send_date = None

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        user = User.objects.get(email=self.to)
        token = ResetPasswordToken.objects.filter(user_id=user.id).last()
        block = ResetPasswordBlockFactory(instance=token)
        self.blocks.add(block)


class VerifyEmailFactory(EmailFactory):
    class Params:
        instance = None

    subject = settings.VERIFY_EMAIL_SUBJECT
    header = settings.VERIFY_EMAIL_HEADER
    to = factory.LazyAttribute(lambda object: f'{object.instance.email}')
    programed_send_date = None

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        user = User.objects.get(email=self.to)
        block = VerifyEmailBlockFactory(user=user)
        self.blocks.add(block)
