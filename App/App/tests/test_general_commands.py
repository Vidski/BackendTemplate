import io
import sys
from contextlib import redirect_stdout

from django.core.management import call_command
from django.test import TestCase

from App.management.commands.populate_db import Command as PopulateCommand
from Emails.models import Email
from Users.factories.user import UserFactory
from Users.models import User


COMMAND = 'populate_db'


class TestPopulateCommand(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Email.objects.all().delete()

    def test_create_fake_users(self):
        command = PopulateCommand()
        assert User.objects.all().count() == 0
        suppress_text = io.StringIO()
        sys.stdout = suppress_text
        command.create_fake_users()
        assert User.objects.all().count() == 50

    def test_create_fake_verify_emails(self):
        command = PopulateCommand()
        users = [UserFactory(), UserFactory()]
        assert User.objects.all().count() == 2
        assert Email.objects.all().count() == 0
        suppress_text = io.StringIO()
        sys.stdout = suppress_text
        command.create_fake_verify_emails(users)
        assert User.objects.all().count() == 2
        assert Email.objects.all().count() == 2

    def test_command(self):
        assert User.objects.all().count() == 0
        assert Email.objects.all().count() == 0
        call_command(COMMAND)
        assert User.objects.all().count() == 50
        assert Email.objects.all().count() == 50
