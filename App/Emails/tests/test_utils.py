import pytest
from django.core import mail
from django_rest_passwordreset.models import ResetPasswordToken

from Emails.models import Block
from Emails.models import Email
from Emails.utils import send_email
from Users.fakers.user import UserFaker
from Users.models import Profile
from Users.models import User


@pytest.fixture(scope='function', autouse=True)
def setUp(django_db_blocker):
    with django_db_blocker.unblock():
        Email.objects.all().delete()
        Block.objects.all().delete()
        User.objects.all().delete()
        Profile.objects.all().delete()


@pytest.mark.django_db
class TestEmailUtils:
    def test_send_email_verify_email(self):
        email_type = 'verify_email'
        user = UserFaker()
        emails = Email.objects.all().count()
        assert emails == 0
        assert len(mail.outbox) == 0
        send_email(email_type, user)
        emails = Email.objects.all().count()
        assert emails == 1
        assert len(mail.outbox) == 1

    def test_reset_password_verify_email(self):
        email_type = 'reset_password'
        user = UserFaker()
        instance = ResetPasswordToken.objects.create(user=user)
        emails = Email.objects.all().count()
        assert emails == 0
        assert len(mail.outbox) == 0
        send_email(email_type, instance)
        emails = Email.objects.all().count()
        assert emails == 1
        assert len(mail.outbox) == 1
