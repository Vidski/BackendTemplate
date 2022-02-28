from Users.factories.user import UserFactory


class UserFaker(UserFactory):
    email = 'normaluser@appname.me'
    phone_number = '+1123123123'


class AdminFaker(UserFactory):
    email = 'adminuser@appname.me'
    phone_number = '+1123123124'
    is_admin = True
    is_verified = True
