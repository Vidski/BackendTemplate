from django.conf import settings
from django.db.models import QuerySet

from Users.models import User
from dataclasses import dataclass

from Users.serializers import UserLoginSerializer
from Users.serializers import UserSignUpSerializer

@dataclass
class RegisterOrLogin:
    provider: str
    user_data: dict

    def __post_init__(self) -> None:
        email: str = self.user_data["email"]
        self.queryset: QuerySet = User.objects.filter(email=email)
        self.serialized_user: dict = self.get_serialized_user()

    @property
    def user_exists(self) -> bool:
        return self.queryset.exists()

    def get_serialized_user(self) -> dict:
        if self.user_exists:
            user: User = self.queryset.first()
            return UserLoginSerializer(user).data
        return self.register_user()

    def register_user(self) -> dict:
        user_data: dict = {
            "first_name": self.user_data["given_name"],
            "last_name": self.user_data["family_name"],
            "email": self.user_data["email"],
            "password": settings.OAUTH_PASSWORD,
            "auth_provider": self.provider,
            "is_verified": True
        }
        user: User = User.objects.create_user(**user_data)
        return UserSignUpSerializer(user).data
