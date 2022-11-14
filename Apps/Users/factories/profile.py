from django.db.models import Model
from factory.django import DjangoModelFactory

from Users.models import Profile


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model: Model = Profile
