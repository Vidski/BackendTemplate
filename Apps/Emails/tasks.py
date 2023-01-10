from celery import shared_task
from django.db.models import QuerySet
from django.utils.timezone import now

from Emails.models import Email
from Emails.models import Notification
from settings.celery_worker import app


SECONDS: float = 10.0


@shared_task
def create_notifications_emails() -> None:
    notifications: QuerySet = Notification.objects.filter(was_sent=False)
    for notification in notifications:
        notification.send()


@shared_task
def send_emails() -> None:
    emails: QuerySet = Email.objects.filter(
        was_sent=False, programed_send_date__lte=now()
    )
    for email in emails:
        email.send()


def each_seconds() -> float:
    return SECONDS


app.conf.beat_schedule = {
    "create_notifications_emails": {
        "task": "Emails.tasks.create_notifications_emails",
        "schedule": each_seconds(),
    },
    "send_emails": {
        "task": "Emails.tasks.send_emails",
        "schedule": each_seconds(),
    },
}
