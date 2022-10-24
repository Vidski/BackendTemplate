import pytest
from rest_framework import serializers

from Users.Auth.serializers import UserLoginSerializer
from Users.Auth.serializers import UserSignUpSerializer
from Users.fakers.user import UserFaker
from Users.models import User


@pytest.mark.django_db
class TestUserLoginSerializer:
    def test_data_serialized_from_data(self) -> None:
        user: User = UserFaker()
        user.verify()
        expected_data: dict = {"email": user.email}
        data: dict = {"email": user.email, "password": "password"}
        actual_data: dict = UserLoginSerializer(data).data
        assert actual_data == expected_data

    def test_validate_fails_with_wrong_email(self) -> None:
        data: dict = {"email": "wrongemail@appname.me", "password": "password"}
        serializer: UserLoginSerializer = UserLoginSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid()

    def test_validate_fails_with_wrong_password(self) -> None:
        data: dict = {
            "email": "normaluser@appname.me",
            "password": "wrongpassword",
        }
        serializer: UserLoginSerializer = UserLoginSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid()

    def test_validate_fails_without_email(self) -> None:
        data: dict = {"password": "password"}
        serializer: UserLoginSerializer = UserLoginSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid()

    def test_validate_fails_without_password(self) -> None:
        data: dict = {"email": "normaluser@appname.me"}
        serializer: UserLoginSerializer = UserLoginSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid()

    def test_validate_passes_fails_with_user_not_verified(self) -> None:
        data: dict = {"email": "normaluser@appname.me", "password": "password"}
        serializer: UserLoginSerializer = UserLoginSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid()

    def test_validate_passes_with_right_data(self) -> None:
        user: User = UserFaker(
            email="normaluser@appname.me", password="password"
        )
        user.verify()
        data: dict = {"email": "normaluser@appname.me", "password": "password"}
        serializer: UserLoginSerializer = UserLoginSerializer(data=data)
        serializer.is_valid()

    def test_create_function(self) -> None:
        user: User = UserFaker(
            email="normaluser@appname.me", password="password"
        )
        user.verify()
        data: dict = {"email": "normaluser@appname.me", "password": "password"}
        serializer: UserLoginSerializer = UserLoginSerializer(data=data)
        serializer.is_valid()
        data: dict = serializer.data
        assert data["email"] == user.email
        assert data["id"] == user.id
        assert data["token"] is not None
        assert data["refresh_token"] is not None


@pytest.mark.django_db
class TestUserSignUpSerializer:
    def test_data_serialized_from_data(self) -> None:
        data: dict = {
            "first_name": "Name",
            "last_name": "Lastname",
            "email": "newuser@appname.me",
            "password": "non_common_password",
            "password_confirmation": "non_common_password",
        }
        expected_data: dict = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
        }
        serializer: UserSignUpSerializer = UserSignUpSerializer(data=data)
        serializer.is_valid()
        actual_data: dict = serializer.data
        assert actual_data == expected_data

    def test_validate_fails_with_wrong_email(self) -> None:
        data: dict = {
            "first_name": "Name",
            "last_name": "Lastname",
            "email": "wrong",
        }
        serializer: UserSignUpSerializer = UserSignUpSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_fails_with_wrong_password(self) -> None:
        data: dict = {
            "first_name": "Name",
            "last_name": "Lastname",
            "email": "email@appname.me",
            "password": "wrongpassword",
            "password_confirmation": "Wrong_password",
        }
        serializer: UserSignUpSerializer = UserSignUpSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_fails_with_missing_password_confirmation(self) -> None:
        data: dict = {
            "first_name": "Name",
            "last_name": "Lastname",
            "email": "email@appname.me",
            "password": "wrong",
        }
        serializer: UserSignUpSerializer = UserSignUpSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_fails_with_common_password(self) -> None:
        data: dict = {
            "first_name": "Name",
            "last_name": "Lastname",
            "email": "email@appname.me",
            "password": "123456",
            "password_confirmation": "123456",
        }
        serializer: UserSignUpSerializer = UserSignUpSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_is_successful(self) -> None:
        data: dict = {
            "first_name": "Name",
            "last_name": "Lastname",
            "email": "email@appname.me",
            "password": "strong password 123",
            "password_confirmation": "strong password 123",
        }
        serializer: UserSignUpSerializer = UserSignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)

    def test_create_function(self) -> None:
        serializer: UserSignUpSerializer = UserSignUpSerializer()
        data: dict = {
            "first_name": "Name",
            "last_name": "Lastname",
            "email": "email@appname.me",
            "password": "strong password 123",
            "password_confirmation": "strong password 123",
        }
        user: User = serializer.create(data)
        assert isinstance(user, User)
        assert user.email == data["email"]
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.is_verified == False
