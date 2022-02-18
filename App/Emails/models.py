from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

TEMPLATE_CHOICES = [
    ('verify_email.html', 'Verify email'),
    ('reset_password.html', 'Reset password'),
    ('email/email.html', 'General'),
]


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
    blocks = models.ManyToManyField(Block, related_name="blocks", blank=True)
    to = models.TextField(blank=True)
    template = models.CharField(
        max_length=100,
        default='General',
        choices=TEMPLATE_CHOICES
    )
    is_test = models.BooleanField(default=False)
    programed_send_date = models.DateTimeField(blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    was_sent = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f'{self.subject} | {self.to}'

    def save(self):
        if self.is_test:
            self.to = f'{settings.TEST_EMAIL},'
        if self.programed_send_date is None:
            self.programed_send_date = timezone.now()
        super().save()

    def get_to_emails(self):
        return self.to.split(',')

    def get_blocks(self):
        blocks = []
        for block in self.blocks.all():
            block = {
                'title': block.title,
                'content': block.content,
                'show_link': block.show_link,
                'link_text': block.link_text,
                'link': block.link,
            }
            blocks.append(block)
        return blocks

    def get_email_data(self):
        data = {
            'header': self.header,
            'blocks': self.get_blocks(),
        }
        return data

    def get_template(self):
        data = self.get_email_data()
        template = render_to_string(self.template, data)
        return template

    def get_email(self):
        email = EmailMultiAlternatives(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            self.get_to_emails(),
        )
        email.attach_alternative(self.get_template(), 'text/html')
        email.fail_silently = False
        return email

    def send(self):
        email = self.get_email()
        email.send()
        self.sent_date =  timezone.now()
        self.was_sent = True
        self.save()
