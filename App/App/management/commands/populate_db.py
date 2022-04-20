import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm
from tqdm import trange as progress

from Emails.factories.email import SuggestionEmailFactory
from Emails.factories.email import VerifyEmailFactory
from Users.factories.profile import ProfileFactory
from Users.factories.user import UserFactory


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Populate database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--instances', type=int, default=50)

    def handle(self, *args, **options):
        instances = options['instances']
        if settings.ENVIRONMENT_NAME in ['dev', 'local', 'test']:
            self.populate(instances)
        else:
            logger.critical(
                'This command creates fake data do NOT run this in'
                + ' production environments'
            )

    def populate(self, instances):
        users = self.create_fake_users(instances)
        self.create_fake_verify_emails(users)
        self.create_fake_profiles(users)
        self.create_fake_suggestions(users)

    def create_fake_users(self, instances):
        self.stdout.write('Creating fake users')
        users = []
        for _ in progress(instances):
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
        self.stdout.write('Fake verify emails created')

    def create_fake_profiles(self, users):
        self.stdout.write('Creating fake profiles')
        with tqdm(total=len(users)) as progress_bar:
            for user in users:
                ProfileFactory(user=user)
                progress_bar.update(1)
        self.stdout.write('Fake profiles created')

    def create_fake_suggestions(self, users):
        self.stdout.write('Creating fake suggestions')
        type = 'SUGGESTION'
        content = 'This is a fake suggestion'
        with tqdm(total=len(users)) as progress_bar:
            for user in users:
                SuggestionEmailFactory(type=type, content=content, user=user)
                progress_bar.update(1)
        self.stdout.write('Fake profiles created')
