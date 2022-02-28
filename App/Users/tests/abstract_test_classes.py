from django.test import TestCase
from rest_framework.test import APIClient

from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


class UsersAbstractUtils(TestCase):
    def setUp(self):
        self._clean()
        self.admin_user = AdminFaker()
        self.normal_user = UserFaker()
        self.client = APIClient()

    def _clean(self):
        User.objects.all().delete()
