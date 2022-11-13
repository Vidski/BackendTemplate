import pytest
from mock import patch
from mock.mock import MagicMock

from Users.Auth.serializers import UserAuthSerializer
from Users.Auth.serializers import UserLoginSerializer
from Users.Auth.serializers import UserSignUpSerializer
from Users.fakers.user import UserFaker
from Users.models import User
from Users.OAuth.user_handler import RegisterOrLogin
from Users.OAuth.user_handler import RegisterOrLoginViaFacebook
from Users.OAuth.user_handler import RegisterOrLoginViaGoogle
from Users.OAuth.user_handler import RegisterOrLoginViaTwitter


@pytest.mark.django_db
class TestRegisterOrLoginDataClass:
    @patch("Users.OAuth.user_handler.RegisterOrLogin.get_serialized_user")
    def test_post_init_calls_get_serialized_user(
        self, get_serialized_user: MagicMock
    ) -> None:
        user_data: dict = {"email": "test@email.com"}
        RegisterOrLogin(user_data)
        get_serialized_user.assert_called_once()

    def test_user_exists_returns_true(self) -> None:
        user: User = UserFaker()
        user_data: dict = {"email": f"{user.email}"}
        object: RegisterOrLogin = RegisterOrLogin(user_data)
        assert object.user_exists

    @patch("Users.OAuth.user_handler.RegisterOrLogin.get_serialized_user")
    def test_user_exists_returns_false(
        self, get_serialized_user: MagicMock
    ) -> None:
        user_data: dict = {"email": "test@email.com"}
        object: RegisterOrLogin = RegisterOrLogin(user_data)
        assert not object.user_exists
        get_serialized_user.assert_called_once()

    def test_get_serialized_user_login_serialized(self) -> None:
        user: User = UserFaker()
        user_data: dict = {"email": f"{user.email}"}
        object: RegisterOrLogin = RegisterOrLogin(user_data)
        del object.serialized_user["token"]
        del object.serialized_user["refresh_token"]
        user: User = User.objects.get(email=user.email)
        expected_data: dict = UserAuthSerializer(user).data
        del expected_data["token"]
        del expected_data["refresh_token"]
        assert object.serialized_user == expected_data

    def test_get_user_creation_data_raises_not_implemented_error(self) -> None:
        user_data: dict = {"email": "test@test.com"}
        with pytest.raises(NotImplementedError):
            RegisterOrLogin(user_data)


@pytest.mark.django_db
class TestRegisterOrLoginViaGoogle:
    def test_get_serialized_user_sign_up_serialized(self) -> None:
        user_data: dict = {
            "email": "test@test.com",
            "given_name": "test",
            "family_name": "test",
            "preferred_language": "ES",
        }
        object: RegisterOrLoginViaGoogle = RegisterOrLoginViaGoogle(user_data)
        user: User = User.objects.get(email=user_data["email"])
        object: RegisterOrLogin = RegisterOrLogin(user_data)
        del object.serialized_user["token"]
        del object.serialized_user["refresh_token"]
        user: User = User.objects.get(email=user.email)
        expected_data: dict = UserAuthSerializer(user).data
        del expected_data["token"]
        del expected_data["refresh_token"]
        assert object.serialized_user == expected_data


@pytest.mark.django_db
class TestRegisterOrLoginViaFacebook:
    def test_get_serialized_user_sign_up_serialized(self) -> None:
        user_data: dict = {
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "preferred_language": "ES",
        }
        object: RegisterOrLoginViaFacebook = RegisterOrLoginViaFacebook(
            user_data
        )
        user: User = User.objects.get(email=user_data["email"])
        object: RegisterOrLogin = RegisterOrLogin(user_data)
        del object.serialized_user["token"]
        del object.serialized_user["refresh_token"]
        user: User = User.objects.get(email=user.email)
        expected_data: dict = UserAuthSerializer(user).data
        del expected_data["token"]
        del expected_data["refresh_token"]
        assert object.serialized_user == expected_data


@pytest.mark.django_db
class TestRegisterOrLoginViaTwitter:
    def test_get_serialized_user_sign_up_serialized(self) -> None:
        user_data: dict = {
            "email": "test@test.com",
            "name": "test",
            "preferred_language": "ES",
        }
        object: RegisterOrLoginViaTwitter = RegisterOrLoginViaTwitter(user_data)
        user: User = User.objects.get(email=user_data["email"])
        object: RegisterOrLogin = RegisterOrLogin(user_data)
        del object.serialized_user["token"]
        del object.serialized_user["refresh_token"]
        user: User = User.objects.get(email=user.email)
        expected_data: dict = UserAuthSerializer(user).data
        del expected_data["token"]
        del expected_data["refresh_token"]
        assert object.serialized_user == expected_data
