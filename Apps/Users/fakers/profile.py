from datetime import datetime

import factory
from dateutil.relativedelta import relativedelta
from django.db.models import ImageField

from Users.factories.profile import ProfileFactory
from Users.fakers.user import UserFaker
from Users.models import User


class BaseProfileFaker(ProfileFactory):
    user: User = factory.SubFactory(UserFaker)
    image: ImageField = factory.django.ImageField(
        filename="profile_picture.jpg",
        width=100,
        height=100,
        format="JPEG",
        color="gray",
    )
    gender: str = factory.fuzzy.FuzzyChoice(("F", "M", "N", "P"))
    birth_date: datetime = factory.Faker("date")


class FemaleProfileFaker(BaseProfileFaker):
    nickname: str = factory.Faker("name_female")
    bio: str = "Custom bio for female profile"
    gender: str = "F"


class MaleProfileFaker(BaseProfileFaker):
    nickname: str = factory.Faker("name_male")
    bio: str = "Custom bio for male profile"
    gender: str = "M"


class NonBinaryProfileFaker(BaseProfileFaker):
    nickname: str = factory.Faker("name_nonbinary")
    bio: str = "Custom bio for non-binary profile"
    gender: str = "N"


class NotSaidProfileFaker(BaseProfileFaker):
    nickname: str = factory.Faker("suffix")
    bio: str = "Custom bio for x profile"
    gender: str = "P"


class AdultProfileFaker(BaseProfileFaker):
    nickname: str = factory.Faker("isbn13")
    bio: str = "Custom bio for adult profile"
    birth_date: datetime = factory.LazyAttribute(
        lambda object: (
            (datetime.now() - relativedelta(years=20)).strftime("%Y-%m-%d")
        )
    )


class KidProfileFaker(BaseProfileFaker):
    nickname: str = factory.Faker("isbn13")
    bio: str = "Custom bio for kid profile"
    birth_date: datetime = factory.LazyAttribute(
        lambda object: (
            (datetime.now() - relativedelta(years=15)).strftime("%Y-%m-%d")
        )
    )
