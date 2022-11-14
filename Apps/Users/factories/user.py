from django.db.models import Model
from factory import PostGenerationMethodCall
from factory import post_generation
from factory.django import DjangoModelFactory

from Users.choices import PreferredLanguageChoices
from Users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model: Model = User
        django_get_or_create: tuple = ("email",)

    password: str = PostGenerationMethodCall("set_password", "password")
    is_admin: bool = False
    is_verified: bool = False
    email: str = ""
    preferred_language: str = ""

    @post_generation
    def set_email(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        if create and self.email == "":
            raise ValueError("Email is required")

    @post_generation
    def set_preferred_language(
        self, create: bool, extracted: Model, **kwargs: dict
    ) -> None:
        if create:
            language: str = self.preferred_language
            if not language or language not in PreferredLanguageChoices.values:
                language = PreferredLanguageChoices.ENGLISH
            self.preferred_language = language
