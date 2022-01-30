from Users.tests.abstract_test_classes import UsersAbstractUtils
from Users.factories.user_factories import UserFactory
from Users.serializers import UserSerializer


class TestUserSerializer(UsersAbstractUtils):

    def test_data_serialized_from_user(self):
        user = UserFactory()
        created_at = user.created_at
        updated_at = user.updated_at
        format = '%Y-%m-%dT%H:%M:%S.%fZ'
        expected_created_at = created_at.strftime(format)
        expected_updated_at = updated_at.strftime(format)
        expected_data = {
            'first_name': user.first_name,
            'phone_number': user.phone_number,
            'email': user.email,
            'created_at': expected_created_at,
            'updated_at': expected_updated_at,
        }
        actual_data = UserSerializer(user).data
        self.assertEqual(actual_data, expected_data)
