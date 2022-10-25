import factory

from Emails.factories.blacklist import BlackListFactory
from Users.fakers.user import UserFaker
from Users.models import User


class BlackListFaker(BlackListFactory):
    user: User = factory.SubFactory(UserFaker)
    affairs: str = "PROMOTION"
