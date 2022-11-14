from mock import MagicMock
from mock import PropertyMock
from pytest import mark
from pytest import raises
from rest_framework import serializers

from Users.fakers.user import UserFaker
from Users.models import User
from Users.serializers import UserUpdateSerializer


@mark.django_db
class TestUserUpdateSerializer:
    def test_data_serialized_from_user(self) -> None:
        user: User = UserFaker()
        expected_data: dict = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "email": user.email,
        }
        actual_data: dict = UserUpdateSerializer(user).data
        assert actual_data == expected_data

    def test_check_password_return_None_if_not_password(self) -> None:
        user: User = UserFaker()
        data: dict = {
            "password": None,
        }
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        serializer.is_valid(raise_exception=True)

    def test_check_password_fails_without_old_password(self) -> None:
        user: User = UserFaker()
        data: dict = {
            "password": "newpassword",
        }
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        with raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_check_password_fails_with_wrong_old_password(self) -> None:
        user: User = UserFaker()
        data: dict = {
            "password": "newpassword",
            "old_password": "wrongpassword",
        }
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        with raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_check_password_fails_with_common_password(self) -> None:
        user: User = UserFaker()
        data: dict = {
            "password": "123456",
            "old_password": "password",
        }
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        with raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_check_password_passes_with_right_old_password_and_no_common_new_password(
        self,
    ) -> None:
        user: User = UserFaker()
        data: dict = {
            "password": "Strong Password 123",
            "old_password": "password",
        }
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        serializer.is_valid(raise_exception=True)

    def test_check_phone_number_fails_with_existing_phone_number(self) -> None:
        phone_number: str = "+1123123123"
        UserFaker(phone_number=phone_number)
        user: User = UserFaker()
        data: dict = {"phone_number": "+1123123123"}
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        with raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_check_phone_number_return_None_if_not_phone_number(self) -> None:
        user: User = UserFaker()
        data: dict = {
            "phone_number": None,
        }
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        serializer.is_valid(raise_exception=True)

    def test_check_phone_number_passes(self) -> None:
        user: User = UserFaker()
        data: dict = {"phone_number": "+1123123123"}
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        serializer.is_valid(raise_exception=True)

    def test_check_email_fails_with_existing_email(self) -> None:
        email: str = "normaluser@appname.me"
        UserFaker(email=email)
        user: User = UserFaker()
        data: dict = {"email": email}
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        with raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_check_email_passes(self) -> None:
        user: User = UserFaker()
        email: str = "normaluser2@appname.me"
        data: dict = {"email": email}
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        serializer.is_valid(raise_exception=True)

    def test_update(self) -> None:
        user: User = UserFaker()
        data: dict = {
            "first_name": "newfirstname",
            "last_name": "newlastname",
            "phone_number": "+123123124",
            "email": "newemail@appname.me",
            "password": "new_password",
            "old_password": "password",
        }
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=user)
        type(request).user = mocked_requester
        serializer.context["request"] = request
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        user.refresh_from_db()
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.phone_number == data["phone_number"]
        assert user.email == data["email"]
        assert user.check_password(data["password"]) == True

    def test_is_valid_fails_with_phone_number_with_bad_format(self) -> None:
        UserFaker(phone_number="+1123123123")
        data: dict = {"phone_number": "123123123"}
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=data)
        with raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
