import factory
import factory.fuzzy
from django.db.models import Model

from Users.models import Profile


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = Profile
