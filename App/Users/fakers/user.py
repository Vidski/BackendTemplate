import factory

from Users.factories.user import UserFactory


class UserFaker(UserFactory):
    phone_number = '+1123123123'


class VerifiedUserFaker(UserFaker):
    phone_number = factory.Faker('msisdn')
    is_verified = True


class AdminFaker(UserFactory):
    phone_number = '+1123123124'
    is_admin = True
    is_verified = True
