import factory
from Emails.models.models import BlackList
from Emails.models.models import Email

from django.db.models import Model


class BlackListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = BlackList

    email: Email = factory.Faker("email")
