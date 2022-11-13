from abc import abstractmethod
from dataclasses import dataclass

from django.conf import settings
from django.db.models import QuerySet

from Users.Auth.serializers import UserAuthSerializer
from Users.models import User


@dataclass
class RegisterOrLogin:
    user_data: dict

    def __post_init__(self) -> None:
        self.email: str = self.user_data["email"]
        self.queryset: QuerySet = User.objects.filter(email=self.email)
        self.serialized_user: dict = self.get_serialized_user()

    @property
    def user_exists(self) -> bool:
        return self.queryset.exists()

    def get_serialized_user(self) -> dict:
        if self.user_exists:
            user: User = self.queryset.first()
            return UserAuthSerializer(user).data
        return self.register_user()

    def register_user(self) -> dict:
        creation_data: dict = self.get_user_creation_data()
        user: User = User.objects.create_user(**creation_data)
        user.create_profile()
        user.verify()
        return UserAuthSerializer(user).data

    def get_default_data(self) -> dict:
        return {
            "password": settings.OAUTH_PASSWORD,
            "auth_provider": self.provider,
            "email": self.email,
            "preferred_language": self.user_data["preferred_language"],
        }

    @abstractmethod
    def get_user_creation_data(self) -> dict:
        raise NotImplementedError


class RegisterOrLoginViaGoogle(RegisterOrLogin):
    provider: str = "google"

    def get_user_creation_data(self) -> dict:
        return {
            "first_name": self.user_data["given_name"],
            "last_name": self.user_data["family_name"],
            **self.get_default_data(),
        }


class RegisterOrLoginViaFacebook(RegisterOrLogin):
    provider: str = "facebook"

    def get_user_creation_data(self) -> dict:
        return {
            "first_name": self.user_data["first_name"],
            "last_name": self.user_data["last_name"],
            **self.get_default_data(),
        }


class RegisterOrLoginViaTwitter(RegisterOrLogin):
    provider: str = "twitter"

    def get_user_creation_data(self) -> dict:
        return {
            "first_name": self.user_data["name"],
            "last_name": "",
            **self.get_default_data(),
        }
