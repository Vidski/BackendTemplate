from datetime import datetime

import pytest
from rest_framework import serializers

from Users.factories.user import UserFactory
from Users.models import User
from Users.serializers import UserUpdateSerializer


@pytest.mark.django_db
class TestUserUpdateSerializer:
    def test_data_serialized_from_user(self) -> None:
        user: User = UserFactory()
        created_at: datetime = user.created_at
        updated_at: datetime = user.updated_at
        format: str = "%Y-%m-%dT%H:%M:%S.%fZ"
        expected_created_at: datetime = created_at.strftime(format)
        expected_updated_at: datetime = updated_at.strftime(format)
        expected_data: dict = {
            "first_name": user.first_name,
            "phone_number": user.phone_number,
            "email": user.email,
            "created_at": expected_created_at,
            "updated_at": expected_updated_at,
        }
        actual_data: dict = UserUpdateSerializer(user).data
        assert actual_data == expected_data

    def test_check_password_fails_without_old_password(self) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {"password": "newpassword"}
        with pytest.raises(serializers.ValidationError):
            serializer.check_password(data, user)

    def test_check_password_fails_with_wrong_old_password(self) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {
            "password": "newpassword",
            "old_password": "wrongpassword",
        }
        with pytest.raises(serializers.ValidationError):
            serializer.check_password(data, user)

    def test_check_password_fails_with_common_password(self) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {"password": "123456", "old_password": "wrongpassword"}
        with pytest.raises(serializers.ValidationError):
            serializer.check_password(data, user)

    def test_check_password_passes_with_right_old_password_and_no_common_new_password(
        self,
    ) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {
            "password": "Strong Password 123",
            "old_password": "password",
        }
        serializer.check_password(data, user)

    def test_check_phone_number_fails_with_existing_phone_number(self) -> None:
        phone_number: str = "+1123123123"
        UserFactory(phone_number=phone_number)
        new_user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        with pytest.raises(serializers.ValidationError):
            serializer.check_phone_number(phone_number, new_user)

    def test_check_phone_number_passes(self) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        phone_number: str = "+123123124"
        serializer.check_phone_number(phone_number, user)

    def test_check_email_fails_with_existing_email(self) -> None:
        email: str = "normaluser@appname.me"
        UserFactory(email=email)
        new_user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        with pytest.raises(serializers.ValidationError):
            serializer.check_email(email, new_user)

    def test_check_email_passes(self) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        email: str = "normaluser2@appname.me"
        serializer.check_email(email, user)

    def test_update(self) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {
            "first_name": "newfirstname",
            "last_name": "newlastname",
            "phone_number": "+123123124",
            "email": "newemail@appname.me",
            "password": "newpassword",
        }
        serializer.update(user, data)
        user.refresh_from_db()
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.phone_number == data["phone_number"]
        assert user.email == data["email"]
        assert user.check_password(data["password"]) == True

    def test_create(self) -> None:
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {
            "first_name": "newfirstname",
            "last_name": "newlastname",
            "phone_number": "+123123124",
            "email": "newuser@appname.me",
            "password": "newpassword",
        }
        user: User = serializer.create(data)
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.phone_number == data["phone_number"]
        assert user.email == data["email"]
        assert user.check_password(data["password"]) == True

    def test_is_valid_fails_with_email_taken(self) -> None:
        email: str = "normaluser@appname.me"
        UserFactory(email=email)
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {"email": email}
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(data, user)

    def test_is_valid_fails_with_phone_number_taken(self) -> None:
        phone_number: str = "+1123123123"
        UserFactory(phone_number=phone_number)
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {"phone_number": phone_number}
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(data, user)

    def test_is_valid_fails_with_phone_number_with_bad_format(self) -> None:
        user: User = UserFactory(phone_number="+1123123123")
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {"phone_number": "123123123"}
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(data, user)

    def test_is_valid_fails_with_wrong_password(self) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {"password": "wrongpassword"}
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(data, user)

    def test_is_valid_passes_with_valid_data(self) -> None:
        user: User = UserFactory()
        serializer: UserUpdateSerializer = UserUpdateSerializer()
        data: dict = {
            "first_name": "newfirstname",
            "last_name": "newlastname",
            "phone_number": "+123123124",
            "email": "newemail@appname.me",
        }
        serializer.is_valid(data, user)
