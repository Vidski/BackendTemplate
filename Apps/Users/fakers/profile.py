from django.db.models import ImageField
from factory import SubFactory
from factory.django import ImageField

from Users.factories.profile import ProfileFactory
from Users.fakers.user import UserFaker
from Users.models import User


class ProfileFaker(ProfileFactory):
    user: User = SubFactory(UserFaker)
    image: ImageField = ImageField(
        filename="profile_picture.jpg",
        width=100,
        height=100,
        format="JPEG",
        color="gray",
    )
