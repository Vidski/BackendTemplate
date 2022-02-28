import logging
from tqdm import trange as progress

from django.conf import settings
from django.core.management.base import BaseCommand

from Users.factories.user import UserFactory

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Populate database with fake data'

    def handle(self, *args, **options):
        if settings.ENVIRONMENT_NAME in ['dev', 'local', 'test']:
            self.populate_users()
        else:
            logger.critical(
                'This command creates fake data do NOT run this in production environments'
            )

    def populate_users(self):
        self.stdout.write('Creating fake users')
        for _ in progress(50):
            UserFactory()
        self.stdout.write('Fake users created')
