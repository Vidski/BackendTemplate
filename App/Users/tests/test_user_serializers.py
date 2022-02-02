from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied

from Users.tests.abstract_test_classes import UsersAbstractUtils
from Users.factories.user_factories import UserFactory
from Users.serializers import UserAuthSerializer
from Users.serializers import UserLoginSerializer
from Users.serializers import UserSerializer
from Users.serializers import UserSignUpSerializer


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

    def test_comprove_password_fails_without_old_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {
            'password': 'newpassword'
        }
        with self.assertRaises(serializers.ValidationError):
            serializer.comprove_password(data,user)

    def test_comprove_password_fails_with_wrong_old_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {
            'password': 'newpassword',
            'old_password': 'wrongpassword'
        }
        with self.assertRaises(serializers.ValidationError):
            serializer.comprove_password(data,user)

    def test_comprove_password_fails_with_common_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {
            'password': '123456',
            'old_password': 'wrongpassword'
        }
        with self.assertRaises(serializers.ValidationError):
            serializer.comprove_password(data,user)

    def test_comprove_password_passes_with_right_old_password_and_no_common_new_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {
            'password': 'Strong Password 123',
            'old_password': 'password'
        }
        serializer.comprove_password(data,user)

    def test_comprove_phone_number_fails_with_existing_phone_number(self):
        user = UserFactory()
        serializer = UserSerializer()
        phone_number = '123123123'
        with self.assertRaises(serializers.ValidationError):
            serializer.comprove_phone_number(phone_number, user)

    def test_comprove_phone_number_passes(self):
        user = UserFactory()
        serializer = UserSerializer()
        phone_number = '123123124'
        serializer.comprove_phone_number(phone_number, user)

    def test_comprove_email_fails_with_existing_email(self):
        user = UserFactory()
        serializer = UserSerializer()
        email = 'normaluser@appname.me'
        with self.assertRaises(serializers.ValidationError):
            serializer.comprove_email(email, user)

    def test_comprove_email_passes(self):
        user = UserFactory()
        serializer = UserSerializer()
        email = 'normaluser2@appname.me'
        serializer.comprove_email(email, user)

    def test_update(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'phone_number': '123123124',
            'email': 'newemail@appname.me',
            'password': 'newpassword'
        }
        serializer.update(user, data)
        user.refresh_from_db()
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.phone_number, data['phone_number'])
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))