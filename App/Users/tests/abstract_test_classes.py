from App.tests.abstract_test_class import AbstractTestClass
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


class UsersAbstractUtils(AbstractTestClass):
    def setUp(self):
        self._clean()
        self.admin_user = AdminFaker()
        self.normal_user = UserFaker()
        super().setUp()

    def _clean(self):
        User.objects.all().delete()
