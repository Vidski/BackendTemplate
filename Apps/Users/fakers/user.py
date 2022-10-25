import factory
from django.conf import settings
from django.db.models import Model

from Users.factories.user import UserFactory


class UserFaker(UserFactory):
    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")
    email: str = factory.Faker("email")
    phone_number: str = factory.Faker("msisdn")

    @factory.post_generation
    def set_phone_number(
        self, create: bool, extracted: Model, **kwargs: dict
    ) -> None:
        has_extension: bool = str(self.phone_number)[0] == "+"
        if create and not has_extension:
            self.phone_number = f"+1{self.phone_number}"
            self.save()


class VerifiedUserFaker(UserFaker):
    phone_number: str = factory.Faker("msisdn")
    is_verified: bool = True


class AdminFaker(UserFaker):
    phone_number: str = factory.Faker("msisdn")
    is_admin: bool = True
    is_verified: bool = True


class EmailTestUserFaker(UserFaker):
    phone_number: str = "+34123456789"
    is_verified: bool = True
    email: str = settings.TEST_EMAIL
