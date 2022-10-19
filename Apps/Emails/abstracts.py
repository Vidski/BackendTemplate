from abc import abstractmethod
from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Model
from django.template.loader import render_to_string
from django.utils import timezone

from Project.utils.log import log_information


class AbstractEmailFunctionClass:
    @abstractmethod
    def get_email(self) -> str:
        raise NotImplementedError

    def get_email_data(self) -> dict:
        return {
            "header": self.header,
            "blocks": self.blocks.all() if self.blocks.all() else [],
        }

    def get_template(self) -> str:
        data: dict = self.get_email_data()
        template: str = render_to_string("email.html", data)
        return template

    def get_email_object(self) -> EmailMultiAlternatives:
        email: EmailMultiAlternatives = EmailMultiAlternatives(
            subject=self.subject,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.get_email()],
        )
        email.attach_alternative(self.get_template(), "text/html")
        email.fail_silently = False
        return email

    def check_if_email_and_type_is_in_blacklist(self) -> bool:
        blacklist: Model = apps.get_model("Emails", "Blacklist")
        return blacklist.objects.filter(
            user__email=self.get_email(), affairs__icontains=self.affair
        ).exists()

    def send(self) -> None:
        is_email_in_blacklist: bool = (
            self.check_if_email_and_type_is_in_blacklist()
        )
        if not is_email_in_blacklist:
            email: EmailMultiAlternatives = self.get_email_object()
            email.send()
            self.sent_date: datetime = timezone.now()
            self.was_sent: bool = True
            self.save()
        log_information(f"Sent: {self.was_sent}", self)
