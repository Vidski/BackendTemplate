from Users.factories.user import UserFactory


class UserFaker(UserFactory):
    email = 'normaluser@appname.me'
    phone_number = '+1123123123'


class VerifiedUserFaker(UserFaker):
    email = 'normalverifieduser@appname.me'
    is_verified = True


class AdminFaker(UserFactory):
    email = 'adminuser@appname.me'
    phone_number = '+1123123124'
    is_admin = True
    is_verified = True
