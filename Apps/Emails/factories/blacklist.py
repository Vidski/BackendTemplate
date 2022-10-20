import factory
import factory.fuzzy
from django.db.models import Model

from Emails.models import BlackList


class BlackListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = BlackList

    affairs: str = factory.fuzzy.FuzzyChoice(
        (
            "NOTIFICATION",
            "PROMOTION",
            "GENERAL",
            "SETTINGS",
            "INVOICE",
            "SUGGESTION",
        )
    )
