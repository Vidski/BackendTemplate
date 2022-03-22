from django.test import TestCase

from Emails.models import Block
from Emails.models import Email


class EmailsAbstractUtils(TestCase):
    def setUp(self):
        self._clean()

    def _clean(self):
        Block.objects.all().delete()
        Email.objects.all().delete()
