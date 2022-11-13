from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Emails.fakers.blacklist import BlackListFaker
from Emails.models import BlackList
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import User


@fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@mark.django_db
class TestListBlacklistViews:
    def url(self) -> str:
        return reverse("emails:blacklist-list")

    def test_url(self) -> None:
        assert self.url() == "/api/blacklist/"

    def test_list_blacklist_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        url: str = self.url()
        response: Response = client.get(url)
        assert response.status_code == 401

    def test_list_blacklist_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_blacklist_fails_with_normal_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_blacklist_works_with_admin_user(
        self, client: APIClient
    ) -> None:
        user: User = AdminFaker()
        url: str = self.url()
        BlackListFaker.create_batch(15)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 200
        assert response.data["count"] == 15
        assert len(response.data["results"]) == 10


@mark.django_db
class TestRetrieveBlacklistViews:
    def url(self, pk: int = None) -> str:
        return reverse("emails:blacklist-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(pk=1) == "/api/blacklist/1/"

    def test_retrieve_blacklist_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        url: str = self.url()
        response: Response = client.get(url)
        assert response.status_code == 401

    def test_retrieve_blacklist_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_retrieve_blacklist_fails_with_other_normal_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        blacklist: BlackList = BlackListFaker()
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_retrieve_blacklist_works_with_admin_user(
        self, client: APIClient
    ) -> None:
        user: User = AdminFaker()
        blacklist: BlackList = BlackListFaker()
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == blacklist.id

    def test_retrieve_blacklist_works_with_owner_normal_user(
        self, client: APIClient
    ) -> None:
        blacklist: BlackList = BlackListFaker()
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=blacklist.user)
        response: Response = client.get(url)
        assert response.status_code == 403


@mark.django_db
class TestCreateBlacklistViews:
    def url(self) -> str:
        return reverse("emails:blacklist-list")

    def test_url(self) -> None:
        assert self.url() == "/api/blacklist/"

    def test_post_blacklist_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        data: dict = {"user": 2, "affairs": ""}
        url: str = self.url()
        response: Response = client.post(url, data=data)
        assert response.status_code == 401

    def test_post_blacklist_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        data: dict = {"user": 2, "affairs": ""}
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data)
        assert response.status_code == 403

    def test_post_blacklist_fails_with_other_user(
        self, client: APIClient
    ) -> None:
        other_user: User = VerifiedUserFaker()
        data: dict = {"user": other_user.id}
        user: User = VerifiedUserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data)
        assert response.status_code == 403

    def test_post_blacklist_works_with_user(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        data: dict = {"user": user.id}
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data)
        assert response.status_code == 201

    def test_post_blacklist_works_with_admin(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        data: dict = {"user": user.id}
        url: str = self.url()
        client.force_authenticate(user=AdminFaker())
        response: Response = client.post(url, data=data)
        assert response.status_code == 201


@mark.django_db
class TestUpdateBlacklistViews:
    def url(self, pk: int = None) -> str:
        return reverse("emails:blacklist-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(pk=1) == "/api/blacklist/1/"

    def test_post_blacklist_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        blacklist: BlackList = BlackListFaker()
        data: dict = {"user": blacklist.user, "affairs": ""}
        url: str = self.url(pk=blacklist.id)
        response: Response = client.put(url, data=data)
        assert response.status_code == 401

    def test_post_blacklist_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        data: dict = {"user": 2, "affairs": ""}
        user: User = UserFaker()
        blacklist: BlackList = BlackListFaker(user=user)
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.put(url, data=data)
        assert response.status_code == 403

    def test_post_blacklist_fails_with_other_user(
        self, client: APIClient
    ) -> None:
        other_user: User = VerifiedUserFaker()
        data: dict = {"user": other_user.id}
        user: User = VerifiedUserFaker()
        blacklist: BlackList = BlackListFaker(user=user)
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.put(url, data=data)
        assert response.status_code == 403

    def test_post_blacklist_works_with_user(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        blacklist: BlackList = BlackListFaker(user=user)
        data: dict = {"user": user.id}
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.put(url, data=data)
        assert response.status_code == 200

    def test_post_blacklist_works_with_admin(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        blacklist: BlackList = BlackListFaker(user=user)
        other_user: User = VerifiedUserFaker()
        data: dict = {"user": other_user.id}
        url: str = self.url(blacklist.id)
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        response: Response = client.put(url, data=data)
        assert response.status_code == 200


@mark.django_db
class TestDeleteBlacklistViews:
    def url(self, pk: int = None) -> str:
        return reverse("emails:blacklist-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(pk=1) == "/api/blacklist/1/"

    def test_delete_blacklist_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        blacklist: BlackList = BlackListFaker()
        url: str = self.url(pk=blacklist.id)
        response: Response = client.delete(url)
        assert response.status_code == 401

    def test_delete_blacklist_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        blacklist: BlackList = BlackListFaker(user=user)
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.delete(url)
        assert response.status_code == 403

    def test_delete_blacklist_fails_with_other_user(
        self, client: APIClient
    ) -> None:
        other_user: User = VerifiedUserFaker()
        user: User = VerifiedUserFaker()
        blacklist: BlackList = BlackListFaker(user=user)
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=other_user)
        response: Response = client.delete(url)
        assert response.status_code == 403

    def test_delete_blacklist_works_with_user(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        blacklist: BlackList = BlackListFaker(user=user)
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.delete(url)
        assert response.status_code == 204

    def test_delete_blacklist_works_with_admin(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        blacklist: BlackList = BlackListFaker(user=user)
        url: str = self.url(blacklist.id)
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        response: Response = client.delete(url)
        assert response.status_code == 204
