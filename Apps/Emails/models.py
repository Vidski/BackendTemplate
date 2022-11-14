from datetime import datetime

from django.conf import settings
from django.db.models import CASCADE
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models import TextField
from django.db.models import URLField
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignObject
from django.utils import timezone
from django.utils.timezone import now
from django.utils.timezone import timedelta
from django_mysql.models import ListCharField
from django_prometheus.models import ExportModelOperationsMixin

from Emails import factories
from Emails.abstracts import AbstractEmailFunctionClass
from Emails.choices import CommentType
from Emails.choices import EmailAffair
from Project.utils.translation import get_translation_in
from Users.choices import PreferredLanguageChoices
from Users.fakers.user import EmailTestUserFaker
from Users.models import User


class Block(Model):
    """
    Block models will be used as small parts that an email can have,
    allowing this way to create a more dynamic emails according to the
    topic of the email.
    """

    title: Field = CharField(max_length=100, null=True)
    content: Field = TextField(null=True)
    show_link: Field = BooleanField(default=False)
    link_text: Field = CharField(max_length=100, null=True, blank=True)
    link: Field = URLField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.title}"


class Email(
    ExportModelOperationsMixin("email"), Model, AbstractEmailFunctionClass
):

    header: Field = CharField(max_length=100, null=True)
    affair: Field = CharField(
        max_length=100,
        choices=EmailAffair.choices,
        default=EmailAffair.NOTIFICATION.value,
    )
    sent_date: Field = DateTimeField(null=True)
    was_sent: Field = BooleanField(default=False, editable=False)
    blocks: Field = ManyToManyField(
        "Emails.Block", related_name="%(class)s_blocks"
    )
    subject: Field = CharField(max_length=100)
    is_test: Field = BooleanField(default=False)
    programed_send_date: Field = DateTimeField(null=True)
    to: ForeignObject = ForeignKey(
        User, on_delete=CASCADE, null=False, related_name="to_user"
    )
    language: Field = CharField(
        "Preferred language",
        max_length=2,
        choices=PreferredLanguageChoices.choices,
        default=PreferredLanguageChoices.ENGLISH,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.subject}"

    def get_email(self) -> str:
        return self.to.email

    def set_programed_send_date(self) -> None:
        if not self.programed_send_date or self.programed_send_date <= now():
            five_minutes_ahead: datetime = now() + timedelta(minutes=5)
            self.programed_send_date = five_minutes_ahead

    def get_email_data(self) -> dict:
        return {
            **super().get_email_data(),
            "follow_text": get_translation_in(
                self.language, settings.FOLLOW_TEXT
            ),
            "unsubscribe_text": get_translation_in(
                self.language, settings.UNSUBSCRIBE_TEXT
            ),
        }

    def save(self, *args: tuple, **kwargs: dict) -> None:
        if self.is_test:
            self.to = EmailTestUserFaker()
        if not self.was_sent:
            self.set_programed_send_date()
        super(Email, self).save(*args, **kwargs)


class Suggestion(
    ExportModelOperationsMixin("suggestion"), Model, AbstractEmailFunctionClass
):

    header: Field = CharField(max_length=100, null=True)
    affair: Field = CharField(
        max_length=100,
        choices=EmailAffair.choices,
        default=EmailAffair.NOTIFICATION.value,
    )
    sent_date: Field = DateTimeField(null=True)
    was_sent: Field = BooleanField(default=False, editable=False)
    blocks: Field = ManyToManyField(
        "Emails.Block", related_name="%(class)s_blocks"
    )
    user: ForeignObject = ForeignKey(
        User, on_delete=CASCADE, related_name="suggestion", unique=False
    )
    subject: Field = CharField(
        max_length=100,
        choices=CommentType.choices,
        default=CommentType.SUGGESTION.value,
    )
    was_read: Field = BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id} | {self.subject}"

    def get_email(self) -> str:
        return settings.SUGGESTIONS_EMAIL


class Notification(Model, AbstractEmailFunctionClass):

    header: Field = CharField(max_length=100, null=True)
    affair: Field = CharField(
        max_length=100,
        choices=EmailAffair.choices,
        default=EmailAffair.NOTIFICATION.value,
    )
    sent_date: Field = DateTimeField(null=True)
    was_sent: Field = BooleanField(default=False, editable=False)
    blocks: Field = ManyToManyField(
        "Emails.Block", related_name="%(class)s_blocks"
    )
    subject: Field = CharField(max_length=100)
    is_test: Field = BooleanField(default=False)
    programed_send_date: Field = DateTimeField(null=True)
    language: Field = CharField(
        "Preferred language",
        max_length=2,
        choices=PreferredLanguageChoices.choices,
        default=PreferredLanguageChoices.ENGLISH,
        null=True,
    )

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
            if user.preferred_language == self.language:
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


class BlackList(ExportModelOperationsMixin("blacklist"), Model):
    """
    BlackList model, if one user is in this list with given affair, the email
    will not be sent
    """

    user: ForeignObject = ForeignKey(
        User, on_delete=CASCADE, related_name="blacklist", unique=False
    )
    affairs: ListCharField = ListCharField(
        base_field=CharField(
            max_length=15,
            choices=EmailAffair.choices,
            default=EmailAffair.GENERAL.value,
        ),
        size=5,
        max_length=(5 * 15 + 4),  # Base fields per sizer plus commas
    )
