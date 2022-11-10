import factory
from django.db.models import Model

from Users.choices import PreferredLanguageChoices
from Users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = User
        django_get_or_create: tuple = ("email",)

    password: str = factory.PostGenerationMethodCall("set_password", "password")
    is_admin: bool = False
    is_verified: bool = False
    email: str = ""
    preferred_language: str = ""

    @factory.post_generation
    def set_email(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        if create and self.email == "":
            raise ValueError("Email is required")

    @factory.post_generation
    def set_preferred_language(
        self, create: bool, extracted: Model, **kwargs: dict
    ) -> None:
        if create:
            language = self.preferred_language
            if not language or language not in PreferredLanguageChoices.values:
                language = PreferredLanguageChoices.ENGLISH
            self.preferred_language = language
