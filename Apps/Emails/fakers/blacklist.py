from factory import SubFactory

from Emails.factories.blacklist import BlackListFactory
from Users.fakers.user import UserFaker
from Users.models import User


class BlackListFaker(BlackListFactory):
    user: User = SubFactory(UserFaker)
    affairs: str = "PROMOTION"
