import io
import sys
from contextlib import redirect_stdout

from django.core.management import call_command
from django.test import TestCase

from App.management.commands.populate_db import Command as PopulateCommand
from Emails.models import Email
from Users.factories.user import UserFactory
from Users.models import Profile
from Users.models import User


COMMAND = 'populate_db'


class TestPopulateCommand(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Email.objects.all().delete()
        Profile.objects.all().delete()

    def test_create_fake_users(self):
        command = PopulateCommand()
        assert User.objects.all().count() == 0
        suppress_text = io.StringIO()
        sys.stdout = suppress_text
        command.create_fake_users(3)
        assert User.objects.all().count() == 3

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

    def test_create_fake_profiles(self):
        command = PopulateCommand()
        users = [UserFactory(), UserFactory()]
        assert User.objects.all().count() == 2
        assert Profile.objects.all().count() == 0
        suppress_text = io.StringIO()
        sys.stdout = suppress_text
        command.create_fake_profiles(users)
        assert User.objects.all().count() == 2
        assert Profile.objects.all().count() == 2

    def test_command(self):
        assert User.objects.all().count() == 0
        assert Email.objects.all().count() == 0
        assert Profile.objects.all().count() == 0
        call_command(COMMAND, '-i', '5')
        assert User.objects.all().count() == 5
        assert Email.objects.all().count() == 5
        assert Profile.objects.all().count() == 5
