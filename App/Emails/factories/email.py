import factory

from django_rest_passwordreset.models import ResetPasswordToken
from django.utils import timezone

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
        "date_time", tzinfo=timezone.get_current_timezone()
    )
    sent_date = factory.Faker(
        "date_time", tzinfo=timezone.get_current_timezone()
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
