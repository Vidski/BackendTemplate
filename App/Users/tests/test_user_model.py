from Users.factories.user_factories import UserFactory
from Users.tests.abstract_test_classes import UsersAbstractUtils
from Users.models import User


class UserModelTest(UsersAbstractUtils):
    def test_model_has_attributes(self):
        user = UserFactory()
        assert hasattr(user, 'email')
        assert hasattr(user, 'first_name')
        assert hasattr(user, 'last_name')
        assert hasattr(user, 'password')
        assert hasattr(user, 'is_verified')
        assert hasattr(user, 'is_premium')
        assert hasattr(user, 'is_admin')
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')

    def test_model_has_attributes(self):
        user = UserFactory()
        assert user.username == None
        assert user.is_superuser == None
        assert user.last_login == None

    def test_model_has_custom_properties(self):
        user = UserFactory()
        assert user.name == user.first_name + ' ' + user.last_name
        assert user.is_staff == user.is_admin

    def test_model_verify_function(self):
        user = UserFactory()
        assert user.is_verified == False
        user.verify()
        assert user.is_verified == True

    def test_generate_verification_token_function(self):
        user = UserFactory()
        token = user.generate_verification_token()
        assert type(token) == str
        assert len(token) > 10

    def test_has_permission_returns_true(self):
        user = UserFactory()
        user2 = UserFactory()
        has_permission = user.has_permission(user2)
        assert has_permission == False

    def test_has_permission_returns_true(self):
        user = UserFactory()
        has_permission = user.has_permission(user)
        assert has_permission == True
