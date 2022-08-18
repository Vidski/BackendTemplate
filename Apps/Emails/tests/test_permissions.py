import pytest
from django.http import Http404
from mock import MagicMock
from mock import PropertyMock

from Emails.fakers.blacklist import BlackListTestFaker
from Emails.models.models import BlackList
from Emails.permissions import HasListBlacklistPermission
from Emails.permissions import IsBlacklistOwner
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


@pytest.mark.django_db
class TestIsBlacklistOwnerPermission:
    def test_returns_false_if_user_not_owns_the_blacklist_item(self) -> None:
        blacklist: BlackList = BlackListTestFaker()
        kwargs: dict = {"kwargs": {"pk": blacklist.id}}
        requester: User = UserFaker()
        request: MagicMock = MagicMock()
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsBlacklistOwner().has_permission(request, None) is False

    def test_returns_true_if_user_owns_the_blacklist_item(self) -> None:
        blacklist: BlackList = BlackListTestFaker()
        kwargs: dict = {"kwargs": {"pk": blacklist.id}}
        requester: User = UserFaker()
        request: MagicMock = MagicMock()
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsBlacklistOwner().has_permission(request, None) is False

    def test_raises_404_if_blacklist_item_does_not_exists(self) -> None:
        kwargs: dict = {"kwargs": {"pk": 123}}
        requester: User = UserFaker()
        request: MagicMock = MagicMock()
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        with pytest.raises(Http404):
            IsBlacklistOwner().has_permission(request, None)


@pytest.mark.django_db
class TestHasListBlacklistPermission:
    def test_returns_true_if_user_is_retrieving_an_element(self) -> None:
        blacklist: BlackList = BlackListTestFaker()
        kwargs: dict = {"kwargs": {"pk": blacklist.id}}
        requester: User = UserFaker()
        request: MagicMock = MagicMock()
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        mocker_method: PropertyMock = PropertyMock(return_value="GET")
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        type(request).method = mocker_method
        assert (
            HasListBlacklistPermission().has_permission(request, None) is True
        )

    def test_returns_false_if_user_is_listing_elements(self) -> None:
        kwargs: dict = {"kwargs": {}}
        requester: User = UserFaker()
        request: MagicMock = MagicMock()
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        mocker_method: PropertyMock = PropertyMock(return_value="GET")
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        type(request).method = mocker_method
        assert (
            HasListBlacklistPermission().has_permission(request, None) is False
        )

    def test_returns_true_if_admin_is_listing_elements(self) -> None:
        kwargs: dict = {"kwargs": {}}
        requester: User = AdminFaker()
        request: MagicMock = MagicMock()
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        mocker_method: PropertyMock = PropertyMock(return_value="GET")
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        type(request).method = mocker_method
        assert (
            HasListBlacklistPermission().has_permission(request, None) is True
        )

    def test_returns_true_if_admin_is_retrieving_an_element(self) -> None:
        blacklist: BlackList = BlackListTestFaker()
        kwargs: dict = {"kwargs": {"pk": blacklist.id}}
        requester: User = AdminFaker()
        request: MagicMock = MagicMock()
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        mocker_method: PropertyMock = PropertyMock(return_value="GET")
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        type(request).method = mocker_method
        assert (
            HasListBlacklistPermission().has_permission(request, None) is True
        )
