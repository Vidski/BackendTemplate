from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignObject
from django.utils import timezone
from django.utils.timezone import now
from django.utils.timezone import timedelta
from django_mysql.models import ListCharField

from Emails import factories
from Emails.abstracts import AbstractEmailFunctionClass
from Emails.choices import CommentType
from Emails.choices import EmailAffair
from Users.fakers.user import EmailTestUserFaker
from Users.models import User


class Block(models.Model):

    title: Field = models.CharField(max_length=100, null=True)
    content: Field = models.TextField(null=True)
    show_link: Field = models.BooleanField(default=False)
    link_text: Field = models.CharField(max_length=100, null=True, blank=True)
    link: Field = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.title}"


class Email(models.Model, AbstractEmailFunctionClass):

    header: Field = models.CharField(max_length=100, null=True)
    affair: Field = models.CharField(
        max_length=100,
        choices=EmailAffair.choices,
        default=EmailAffair.NOTIFICATION.value,
    )
    sent_date: Field = models.DateTimeField(null=True)
    was_sent: Field = models.BooleanField(default=False, editable=False)
    blocks: Field = models.ManyToManyField(
        "Emails.Block", related_name="%(class)s_blocks"
    )
    subject: Field = models.CharField(max_length=100)
    is_test: Field = models.BooleanField(default=False)
    programed_send_date: Field = models.DateTimeField(null=True)
    to: ForeignObject = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name="to_user"
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.subject}"

    def get_email(self) -> str:
        return self.to.email

    def set_programed_send_date(self) -> None:
        if not self.programed_send_date or self.programed_send_date <= now():
            five_minutes_ahead: datetime = now() + timedelta(minutes=5)
            self.programed_send_date = five_minutes_ahead

    def save(self, *args: tuple, **kwargs: dict) -> None:
        if self.is_test:
            self.to = EmailTestUserFaker()
        if not self.was_sent:
            self.set_programed_send_date()
        super(Email, self).save(*args, **kwargs)


class Suggestion(models.Model, AbstractEmailFunctionClass):

    header: Field = models.CharField(max_length=100, null=True)
    affair: Field = models.CharField(
        max_length=100,
        choices=EmailAffair.choices,
        default=EmailAffair.NOTIFICATION.value,
    )
    sent_date: Field = models.DateTimeField(null=True)
    was_sent: Field = models.BooleanField(default=False, editable=False)
    blocks: Field = models.ManyToManyField(
        "Emails.Block", related_name="%(class)s_blocks"
    )
    user: ForeignObject = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="suggestion", unique=False
    )
    subject: Field = models.CharField(
        max_length=100,
        choices=CommentType.choices,
        default=CommentType.SUGGESTION.value,
    )
    was_read: Field = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id} | {self.subject}"

    def get_email(self) -> str:
        return settings.SUGGESTIONS_EMAIL


class Notification(models.Model, AbstractEmailFunctionClass):

    header: Field = models.CharField(max_length=100, null=True)
    affair: Field = models.CharField(
        max_length=100,
        choices=EmailAffair.choices,
        default=EmailAffair.NOTIFICATION.value,
    )
    sent_date: Field = models.DateTimeField(null=True)
    was_sent: Field = models.BooleanField(default=False, editable=False)
    blocks: Field = models.ManyToManyField(
        "Emails.Block", related_name="%(class)s_blocks"
    )
    subject: Field = models.CharField(max_length=100)
    is_test: Field = models.BooleanField(default=False)
    programed_send_date: Field = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.subject}"

    def send(self) -> None:
        if not self.is_test:
            self.create_email_for_every_user()
        self.create_email(to=EmailTestUserFaker())
        self.sent_date: datetime = timezone.now()
        self.was_sent: bool = True
        self.save()

    def create_email_for_every_user(self) -> None:
        for user in User.objects.all():
            self.create_email(user)

    def create_email(self, to: User) -> None:
        factories.email.EmailFactory(
            to=to,
            subject=self.subject,
            header=self.header,
            is_test=self.is_test,
            programed_send_date=self.programed_send_date,
            sent_date=None,
            blocks=self.blocks.all(),
        )


class BlackList(models.Model):
    """
    BlackList model, if one user is in this list with given affair, the email
    will not be sent
    """

    user: ForeignObject = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blacklist", unique=False
    )
    affairs: ListCharField = ListCharField(
        base_field=models.CharField(
            max_length=15,
            choices=EmailAffair.choices,
            default=EmailAffair.GENERAL.value,
        ),
        size=5,
        max_length=(5 * 15 + 4),  # Base fields per sizer plus commas
    )