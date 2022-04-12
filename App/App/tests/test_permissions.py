import pytest
from mock import MagicMock
from mock import PropertyMock

from App.permissions import IsAdmin
from App.permissions import IsProfileOwner
from App.permissions import IsUserOwner
from App.permissions import IsVerified
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker


@pytest.mark.django_db
class TestIsAdminPermission:
    def test_returns_false_if_user_is_not_admin(self):
        requester = UserFaker()
        assert requester.is_admin is False
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsAdmin().has_permission(request, None) is False

    def test_returns_true_if_user_is_admin(self):
        requester = AdminFaker()
        assert requester.is_admin is True
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsAdmin().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsVerifiedPermission:
    def test_returns_false_if_user_is_not_verified(self):
        requester = UserFaker()
        assert requester.is_verified is False
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsVerified().has_permission(request, None) is False

    def test_returns_true_if_user_is_verified(self):
        requester = VerifiedUserFaker()
        assert requester.is_verified is True
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsVerified().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsUserOwnerPermission:
    def test_returns_false_if_user_is_not_owner(self):
        user = UserFaker()
        requester = VerifiedUserFaker()
        request = MagicMock()
        kwargs = {'kwargs': {'pk': user.id}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        type(request).parser_context = mocked_kwargs
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsUserOwner().has_permission(request, None) is False

    def test_returns_true_if_user_is_owner(self):
        requester = VerifiedUserFaker()
        request = MagicMock()
        kwargs = {'kwargs': {'pk': requester.id}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsUserOwner().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsProfileOwnerPermission:
    def test_returns_true_if_profile_is_from_user(self):
        requester = VerifiedUserFaker()
        request = MagicMock()
        kwargs = {'kwargs': {'pk': requester.profile.id}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsProfileOwner().has_permission(request, None) is True

    def test_returns_false_if_profile_is_not_from_user(self):
        requester = VerifiedUserFaker()
        other_user = VerifiedUserFaker(email="other@user.com")
        request = MagicMock()
        kwargs = {'kwargs': {'pk': other_user.profile.id}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsProfileOwner().has_permission(request, None) is False
