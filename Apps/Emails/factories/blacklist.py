from django.db.models import Model
from factory.django import DjangoModelFactory

from Emails.models import BlackList


class BlackListFactory(DjangoModelFactory):
    class Meta:
        model: Model = BlackList
