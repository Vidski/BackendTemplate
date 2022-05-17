from django.conf import settings
from django.db import models
from django.utils import timezone

from Emails.abstracts import AbstractEmailClass
from Emails.choices import CommentType
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
    header = models.CharField(max_length=100, null=True)
    blocks = models.ManyToManyField(Block, related_name='%(class)s_blocks')
    is_test = models.BooleanField(default=False)
    programed_send_date = models.DateTimeField(null=True)
    sent_date = models.DateTimeField(null=True)
    was_sent = models.BooleanField(default=False, editable=False)
    to = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='to_user'
    )

    def get_emails(self):
        return self.to.email

    def save(self, *args, **kwargs):
        if self.programed_send_date is None:
            now = timezone.now()
            five_minutes_from_now = now + timezone.timedelta(minutes=5)
            self.programed_send_date = five_minutes_from_now
        super(Email, self).save(*args, **kwargs)


class Suggestion(AbstractEmailClass):
    """
    Suggestion model
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='suggestion', unique=False
    )
    subject = models.CharField(
        max_length=100,
        choices=CommentType.choices,
        default=CommentType.SUGGESTION.value,
    )
    header = models.CharField(max_length=100, null=True)
    blocks = models.ManyToManyField(Block, related_name='%(class)s_blocks')
    to = models.CharField(
        max_length=100, null=False, default=settings.SUGGESTIONS_EMAIL
    )
    sent_date = models.DateTimeField(null=True)
    was_sent = models.BooleanField(default=False, editable=False)
    was_read = models.BooleanField(default=False)
