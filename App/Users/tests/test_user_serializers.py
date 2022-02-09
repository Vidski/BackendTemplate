from django.core.exceptions import ValidationError
from rest_framework import serializers

from Users.tests.abstract_test_classes import UsersAbstractUtils
from Users.factories.user_factories import UserFactory
from Users.models import User
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

    def test_check_password_fails_without_old_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {'password': 'newpassword'}
        with self.assertRaises(serializers.ValidationError):
            serializer.check_password(data, user)

    def test_check_password_fails_with_wrong_old_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {'password': 'newpassword', 'old_password': 'wrongpassword'}
        with self.assertRaises(serializers.ValidationError):
            serializer.check_password(data, user)

    def test_check_password_fails_with_common_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {'password': '123456', 'old_password': 'wrongpassword'}
        with self.assertRaises(serializers.ValidationError):
            serializer.check_password(data, user)

    def test_check_password_passes_with_right_old_password_and_no_common_new_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {'password': 'Strong Password 123', 'old_password': 'password'}
        serializer.check_password(data, user)

    def test_check_phone_number_fails_with_existing_phone_number(self):
        user = UserFactory()
        serializer = UserSerializer()
        phone_number = '+1123123123'
        with self.assertRaises(serializers.ValidationError):
            serializer.check_phone_number(phone_number, user)

    def test_check_phone_number_passes(self):
        user = UserFactory()
        serializer = UserSerializer()
        phone_number = '+123123124'
        serializer.check_phone_number(phone_number, user)

    def test_check_email_fails_with_existing_email(self):
        user = UserFactory()
        serializer = UserSerializer()
        email = 'normaluser@appname.me'
        with self.assertRaises(serializers.ValidationError):
            serializer.check_email(email, user)

    def test_check_email_passes(self):
        user = UserFactory()
        serializer = UserSerializer()
        email = 'normaluser2@appname.me'
        serializer.check_email(email, user)

    def test_update(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'phone_number': '+123123124',
            'email': 'newemail@appname.me',
            'password': 'newpassword',
        }
        serializer.update(user, data)
        user.refresh_from_db()
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.phone_number, data['phone_number'])
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))

    def test_create(self):
        serializer = UserSerializer()
        data = {
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'phone_number': '+123123124',
            'email': 'newuser@appname.me',
            'password': 'newpassword',
        }
        user = serializer.create(data)
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.phone_number, data['phone_number'])
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))

    def test_is_valid_fails_with_email_taken(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {'email': 'normaluser@appname.me'}
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(data, user)

    def test_is_valid_fails_with_phone_number_taken(self):
        user = UserFactory(phone_number='+1123123123')
        serializer = UserSerializer()
        data = {'phone_number': '+1123123123'}
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(data, user)

    def test_is_valid_fails_with_phone_number_with_bad_format(self):
        user = UserFactory(phone_number='+1123123123')
        serializer = UserSerializer()
        data = {'phone_number': '123123123'}
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(data, user)

    def test_is_valid_fails_with_wrong_password(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {'password': 'wrongpassword'}
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(data, user)

    def test_is_valid_passes_with_valid_data(self):
        user = UserFactory()
        serializer = UserSerializer()
        data = {
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'phone_number': '+123123124',
            'email': 'newemail@appname.me',
        }
        serializer.is_valid(data, user)


class TestUserLoginSerializer(UsersAbstractUtils):
    def test_data_serialized_from_data(self):
        user = UserFactory()
        user.verify()
        expected_data = {'email': user.email}
        data = {'email': user.email, 'password': 'password'}
        actual_data = UserLoginSerializer(data).data
        self.assertEqual(actual_data, expected_data)

    def test_validate_fails_with_wrong_email(self):
        serializer = UserLoginSerializer()
        data = {'email': 'wrongemail@appname.me', 'password': 'password'}
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)

    def test_validate_fails_with_wrong_password(self):
        serializer = UserLoginSerializer()
        data = {'email': 'normaluser@appname.me', 'password': 'wrongpassword'}
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)

    def test_validate_fails_without_email(self):
        serializer = UserLoginSerializer()
        data = {'password': 'password'}
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)

    def test_validate_fails_without_password(self):
        serializer = UserLoginSerializer()
        data = {'email': 'normaluser@appname.me'}
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)

    def test_validate_passes_fails_with_user_not_verified(self):
        serializer = UserLoginSerializer()
        data = {'email': 'normaluser@appname.me', 'password': 'password'}
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)

    def test_validate_passes_with_right_data(self):
        self.normal_user.verify()
        serializer = UserLoginSerializer()
        data = {'email': 'normaluser@appname.me', 'password': 'password'}
        serializer.validate(data)

    def test_check_email_and_password_fails_without_email(self):
        serializer = UserLoginSerializer()
        data = {'password': 'password'}
        with self.assertRaises(serializers.ValidationError):
            serializer.check_email_and_password(data)

    def test_check_email_and_password_fails_without_password(self):
        serializer = UserLoginSerializer()
        data = {'email': 'normaluser@appname.me'}
        with self.assertRaises(serializers.ValidationError):
            serializer.check_email_and_password(data)

    def test_check_email_and_password_passes(self):
        serializer = UserLoginSerializer()
        data = {'email': 'normaluser@appname.me', 'password': 'password'}
        serializer.check_email_and_password(data)

    def test_create_function(self):
        self.normal_user.verify()
        serializer = UserLoginSerializer()
        data = {'email': 'normaluser@appname.me', 'password': 'password'}
        serializer.validate(data)
        user, token = serializer.create(data)
        self.assertEqual(user, self.normal_user)
        assert token is not None


class TestUserSignUpSerializer(UsersAbstractUtils):
    def test_data_serialized_from_data(self):
        data = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'newuser@appname.me',
            'password': 'password',
        }
        expected_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
        }
        actual_data = UserSignUpSerializer(data).data
        self.assertEqual(actual_data, expected_data)

    def test_validate_fails_with_wrong_email(self):
        serializer = UserSignUpSerializer()
        data = {'first_name': 'Name', 'last_name': 'Lastname', 'email': 'wrong'}
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)

    def test_validate_fails_with_wrong_password(self):
        serializer = UserSignUpSerializer()
        data = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'email@appname.me',
            'password': 'wrong',
            'password_confirmation': 'Wrong',
        }
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)

    def test_validate_fails_with_missing_password_confirmation(self):
        serializer = UserSignUpSerializer()
        data = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'email@appname.me',
            'password': 'wrong',
        }
        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data)

    def test_validate_fails_with_common_password(self):
        serializer = UserSignUpSerializer()
        data = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'email@appname.me',
            'password': '123456',
            'password_confirmation': '123456',
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_validate_is_successful(self):
        serializer = UserSignUpSerializer()
        data = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'email@appname.me',
            'password': 'strong password 123',
            'password_confirmation': 'strong password 123',
        }
        serializer.validate(data)

    def test_create_function(self):
        serializer = UserSignUpSerializer()
        data = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'email@appname.me',
            'password': 'strong password 123',
            'password_confirmation': 'strong password 123',
        }
        user = serializer.create(data)
        assert isinstance(user, User)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.is_verified, False)
