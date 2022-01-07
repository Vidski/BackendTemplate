import factory

from Users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
