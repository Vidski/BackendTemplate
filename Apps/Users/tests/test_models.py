from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from Users.factories.profile import ProfileFactory
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import Profile
from Users.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_model_has_attributes(self) -> None:
        user: User = UserFaker()
        assert hasattr(user, "email")
        assert hasattr(user, "first_name")
        assert hasattr(user, "last_name")
        assert hasattr(user, "password")
        assert hasattr(user, "is_verified")
        assert hasattr(user, "is_premium")
        assert hasattr(user, "is_admin")
        assert hasattr(user, "created_at")
        assert hasattr(user, "updated_at")

    def test_model_do_not_has_attributes(self) -> None:
        user: User = UserFaker()
        assert user.username == None
        assert user.is_superuser == None
        assert user.last_login == None

    def test_model_has_custom_properties(self) -> None:
        user: User = UserFaker()
        assert user.name == user.first_name + " " + user.last_name
        assert user.is_staff == user.is_admin

    def test_model_verify_function(self) -> None:
        user: User = UserFaker()
        assert user.is_verified == False
        user.verify()
        assert user.is_verified == True

    def test_has_permission_returns_false(self) -> None:
        user: User = UserFaker()
        user2: User = UserFaker()
        has_permission: bool = user.has_permission(user2)
        assert has_permission == False

    def test_has_permission_returns_true(self) -> None:
        user: User = UserFaker()
        has_permission: bool = user.has_permission(user)
        assert has_permission == True

    def test_create_profile(self) -> None:
        user: User = UserFaker()
        assert getattr(user, "profile", None) is None
        assert Profile.objects.count() == 0
        user.create_profile()
        assert Profile.objects.count() == 1
        assert getattr(user, "profile", None) is not None

    def test_create_profile_does_not_fails_if_profile_already_exists(
        self,
    ) -> None:
        user: User = UserFaker()
        user.create_profile()
        assert Profile.objects.count() == 1
        user.create_profile()
        assert Profile.objects.count() == 1

    def test_create_user_with_default_language(self) -> None:
        user: User = UserFaker()
        assert getattr(user, "preferred_language", None) is not None
        assert user.preferred_language == "EN"

    def test_create_user_with_default_language_if_wrong_passed(self) -> None:
        user: User = UserFaker(preferred_language="WR")
        assert getattr(user, "preferred_language", None) is not None
        assert user.preferred_language == "EN"

    def test_create_user_with_custom_language(self) -> None:
        user: User = UserFaker(preferred_language="ES")
        assert getattr(user, "preferred_language", None) is not None
        assert user.preferred_language == "ES"

    def test_has_module_perms_as_admin(self) -> None:
        user: User = AdminFaker()
        assert user.has_module_perms("Users") == True
        assert user.has_module_perms("Emails") == True
        assert user.has_module_perms("Logs") == True

    def test_has_module_perms_as_not_admin(self) -> None:
        user: User = UserFaker()
        assert user.has_module_perms("Users") == False
        assert user.has_module_perms("Emails") == False
        assert user.has_module_perms("Logs") == False

    def test_str_user(self) -> None:
        user: User = UserFaker()
        assert str(user) == f"{user.email}"

    def test_null_adultness_user_faker(self) -> None:
        assert User.objects.count() == 0
        user: User = UserFaker()
        assert User.objects.count() == 1
        assert user.is_adult == None

    def test_adult_user_faker(self) -> None:
        assert User.objects.count() == 0
        _20_years_ago: datetime = datetime.now() - relativedelta(years=20)
        user: User = UserFaker(birth_date=_20_years_ago.strftime("%Y-%m-%d"))
        assert User.objects.count() == 1
        assert user.is_adult == True

    def test_kid_user_faker(self) -> None:
        assert User.objects.count() == 0
        _17_years_ago: datetime = datetime.now() - relativedelta(years=17)
        user: User = UserFaker(birth_date=_17_years_ago.strftime("%Y-%m-%d"))
        assert User.objects.count() == 1
        assert user.is_adult == False


@pytest.mark.django_db
class TestProfileModel:
    def test_model_has_attributes(self) -> None:
        profile: Profile = ProfileFactory(user=UserFaker())
        dict_keys: dict = profile.__dict__.keys()
        attributes: list = [attribute for attribute in dict_keys]
        assert "user_id" in attributes
        assert "nickname" in attributes
        assert "bio" in attributes
        assert "image" in attributes
        assert "created_at" in attributes
        assert "updated_at" in attributes

    def test_profile_str(self) -> None:
        profile: Profile = ProfileFactory(user=UserFaker())
        expected_str: str = f"User ({profile.user_id}) profile ({profile.pk})"
        assert str(profile) == expected_str
