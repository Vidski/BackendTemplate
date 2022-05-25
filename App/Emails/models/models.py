from django.conf import settings
from django.db import models
from django.utils import timezone

from Emails.choices import CommentType
from Emails.models.abstracts import AbstractEmailClass
from Users.fakers.user import EmailTestUserFaker
from Users.models import User


class Block(models.Model):
    """
    Block model used on email as block content
    """

    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    show_link = models.BooleanField(default=False)
    link_text = models.CharField(max_length=100, null=True)
    link = models.URLField(max_length=100, null=True)

    def __str__(self):
        return f'{self.id} | {self.title}'


class Email(AbstractEmailClass):
    """
    Email model
    """

    subject = models.CharField(max_length=100)
    is_test = models.BooleanField(default=False)
    programed_send_date = models.DateTimeField(null=True)
    to = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='to_user'
    )

    def get_emails(self):
        emails_in_blacklist = BlackList.objects.all().values_list(
            'email', flat=True
        )
        if self.to.email not in emails_in_blacklist:
            return [self.to.email]
        self.delete()

    def save(self, *args, **kwargs):
        if self.is_test:
            self.to = EmailTestUserFaker()
        if self.programed_send_date is None:
            now = timezone.now()
            five_minutes_from_now = now + timezone.timedelta(minutes=5)
            self.programed_send_date = five_minutes_from_now
        super(Email, self).save(*args, **kwargs)


class Suggestion(AbstractEmailClass):
    """
    Suggestion model, emails that will be sent to admin suggestions email
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='suggestion', unique=False
    )
    subject = models.CharField(
        max_length=100,
        choices=CommentType.choices,
        default=CommentType.SUGGESTION.value,
    )
    was_read = models.BooleanField(default=False)

    def get_emails(self):
        return [settings.SUGGESTIONS_EMAIL]


class Notification(AbstractEmailClass):
    """
    Notification model, it creates an email for each user with this data
    """

    subject = models.CharField(max_length=100)
    is_test = models.BooleanField(default=False)
    programed_send_date = models.DateTimeField(null=True)

    def send(self):
        pass


class BlackList(models.Model):
    """
    BlackList model, if an email is in this list, it will not be sent
    """

    email = models.EmailField(unique=True)
