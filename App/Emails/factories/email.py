import factory

from django.conf import settings
from django_rest_passwordreset.models import ResetPasswordToken
from django.utils import timezone

from Emails.factories.block import BlockFactory
from Emails.factories.block import ResetPasswordBlockFactory
from Emails.factories.block import SuggestionBlockFactory
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


class SuggestionEmailFactory(EmailFactory):
    class Params:
        type = None
        content = None
        instance = None

    subject = factory.LazyAttribute(
        lambda object: get_subject_for_suggestion(object.type, object.content)
    )
    header = factory.LazyAttribute(
        lambda object: (
            f'{object.type}'
            + f' {settings.SUGGESTIONS_EMAIL_HEADER}'
            + f' {object.instance.id}'
        )
    )
    to = settings.SUGGESTIONS_EMAIL
    programed_send_date = None

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        subject_splitted = self.subject.split('||')
        type = subject_splitted[0][:-1]
        content = subject_splitted[1][1:]
        self.subject = type
        self.save()
        block = SuggestionBlockFactory(title=self.header, content=content)
        self.blocks.add(block)


def get_subject_for_suggestion(type, content):
    if type not in settings.SUGGESTION_TYPES:
        raise ValueError('Type not allowed')
    return f'{type} || {content.replace("||", "")}'
