from Emails.models import Block
from Emails.models import Email
from Users.tests.abstract_test_classes import UsersAbstractUtils


class EmailsAbstractUtils(UsersAbstractUtils):
    def setUp(self):
        self._clean()
        super().setUp()

    def _clean(self):
        Block.objects.all().delete()
        Email.objects.all().delete()
