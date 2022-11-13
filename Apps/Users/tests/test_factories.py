from pytest import mark
from pytest import raises

from Users.factories.profile import ProfileFactory
from Users.factories.user import UserFactory
from Users.fakers.user import UserFaker
from Users.models import Profile
from Users.models import User


@mark.django_db
class TestUserFactory:
    def test_user_factory(self) -> None:
        assert User.objects.count() == 0
        user: User = UserFactory(email="email@test.com")
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email is not None
        assert user.phone_number is None
        assert user.password is not None
        assert user.check_password("password") is True
        assert user.is_admin is False
        assert user.is_verified is False

    def test_factory_raises_error_without_email(self) -> None:
        with raises(ValueError):
            UserFactory()


@mark.django_db
class TestProfileFactory:
    def test_profile_factory(self) -> None:
        assert Profile.objects.count() == 0
        profile: Profile = ProfileFactory(user=UserFaker())
        assert Profile.objects.count() == 1
        assert profile.user is not None
        assert profile.nickname is None
        assert profile.bio is None
        assert profile.image is not None
        with raises(ValueError):
            profile.image.url
