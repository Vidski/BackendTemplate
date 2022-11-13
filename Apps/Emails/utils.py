from django_rest_passwordreset.models import ResetPasswordToken

from Emails.factories.email import ResetEmailFactory
from Emails.factories.email import VerifyEmailFactory
from Emails.models import Email
from Project.utils.log import log_email_action
from Users.models import User


EMAILS: dict = {
    "verify_email": VerifyEmailFactory,
    "reset_password": ResetEmailFactory,
}


def send_email(email_type: str, instance: User or ResetPasswordToken) -> None:
    email: Email = EMAILS[email_type](instance=instance)
    email.send()
    log_email_action(email_type, instance)
