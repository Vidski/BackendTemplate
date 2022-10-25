import factory
from django.db.models import Model

from Users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = User
        django_get_or_create: tuple = ("email",)

    password: str = factory.PostGenerationMethodCall("set_password", "password")
    is_admin: bool = False
    is_verified: bool = False
    email: str = ""

    @factory.post_generation
    def set_email(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        if create and self.email == "":
            raise ValueError("Email is required")
