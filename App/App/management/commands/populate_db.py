import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm
from tqdm import trange as progress

from Emails.factories.email import VerifyEmailFactory
from Users.factories.user import UserFactory


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Populate database with fake data'

    def handle(self, *args, **options):
        if settings.ENVIRONMENT_NAME in ['dev', 'local', 'test']:
            self.populate()
        else:
            logger.critical(
                'This command creates fake data do NOT run this in'
                + ' production environments'
            )

    def populate(self):
        users = self.create_fake_users()
        self.create_fake_verify_emails(users)

    def create_fake_users(self):
        self.stdout.write('Creating fake users')
        users = []
        for _ in progress(50):
            user = UserFactory()
            users.append(user)
        self.stdout.write('Fake users created')
        return users

    def create_fake_verify_emails(self, users):
        self.stdout.write('Creating fake verify emails')
        with tqdm(total=len(users)) as progress_bar:
            for user in users:
                VerifyEmailFactory(instance=user)
                progress_bar.update(1)
        self.stdout.write('Fake users created')
