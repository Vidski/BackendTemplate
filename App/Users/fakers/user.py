import factory

from Users.factories.user import UserFactory


class UserFaker(UserFactory):
    phone_number = factory.Faker('msisdn')


class VerifiedUserFaker(UserFaker):
    phone_number = factory.Faker('msisdn')
    is_verified = True


class AdminFaker(UserFactory):
    phone_number = factory.Faker('msisdn')
    is_admin = True
    is_verified = True
