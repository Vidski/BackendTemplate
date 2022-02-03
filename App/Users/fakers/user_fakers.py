from Users.factories.user_factories import UserFactory


class UserFaker(UserFactory):
    email = 'normaluser@appname.me'


class AdminFaker(UserFactory):
    email = 'adminuser@appname.me'
    is_admin = True
    is_verified = True
