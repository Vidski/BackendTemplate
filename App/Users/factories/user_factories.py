import factory

from Users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda user: f"{user.first_name}@appname.com")
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_admin = False
    is_verified = False
    phone_number = "123123123"