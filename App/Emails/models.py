from django.db import models


class Block(models.Model):
    """
    Block model used on email as block content
    """

    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    show_link = models.BooleanField(default=False)
    link_text = models.CharField(max_length=100, blank=True)
    link = models.URLField(max_length=100, blank=True)

    def _str_(self):
        return f'{self.title}'


class Email(models.Model):
    """
    Email model
    """

    subject = models.CharField(max_length=100)
    header = models.CharField(max_length=100, blank=True)
    blocks = models.ManyToManyField(Block, blank=True)
    to = models.TextField(blank=True)
    is_test = models.BooleanField(default=False)
    send_date = models.DateTimeField(blank=True)

    def _str_(self):
        return f'{self.subject} | {self.to}'
