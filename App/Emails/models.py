from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from App.utils import log_information
from Users.models import User


class Block(models.Model):
    """
    Block model used on email as block content
    """

    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    show_link = models.BooleanField(default=False)
    link_text = models.CharField(max_length=100, blank=True)
    link = models.URLField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.id} | {self.title}'


class Email(models.Model):
    """
    Email model
    """

    subject = models.CharField(max_length=100)
    header = models.CharField(max_length=100, blank=True)
    blocks = models.ManyToManyField(Block, related_name='blocks', blank=False)
    is_test = models.BooleanField(default=False)
    to_all_users = models.BooleanField(default=False)
    to = models.TextField(blank=True)
    programed_send_date = models.DateTimeField(blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    was_sent = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f'{self.subject}'

    def save(self, *args, **kwargs):
        if self.to_all_users and not self.is_test:
            all_emails = [f'{user.email}' for user in User.objects.all()]
            self.to = ','.join(all_emails)
        if self.is_test:
            self.to = f'{settings.TEST_EMAIL},'
        if self.programed_send_date is None:
            self.programed_send_date = timezone.now() + timezone.timedelta(
                minutes=5
            )
        super(Email, self).save(*args, **kwargs)

    def get_to_emails(self):
        return self.to.split(',')

    def get_email_data(self):
        return {
            'header': self.header,
            'blocks': self.blocks.all() if self.blocks.all() else [],
        }

    def get_template(self):
        data = self.get_email_data()
        template = render_to_string('email.html', data)
        return template

    def get_email(self):
        email = EmailMultiAlternatives(
            subject=self.subject,
            from_email=settings.EMAIL_HOST_USER,
            bcc=self.get_to_emails(),
        )
        email.attach_alternative(self.get_template(), 'text/html')
        email.fail_silently = False
        return email

    def send(self):
        email = self.get_email()
        email.send()
        self.sent_date = timezone.now()
        self.was_sent = True
        self.save()
        log_information('sent', self)
