from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Emails.fakers.notification import NotificationTestFaker
from Emails.models import Block
from Emails.models import Email
from Emails.models import Notification
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import User


@fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@fixture(scope="function")
def data() -> dict:
    return {
        "header": "Email header",
        "affair": "NOTIFICATION",
        "subject": "Email subject",
        "is_test": True,
        "programed_send_date": "2050-12-12T10:59.000",
        "blocks": [
            {
                "title": "Block title",
                "content": "Block content",
                "link_text": "Click here",
                "show_link": True,
                "link": "google.com",
            }
        ],
    }


@mark.django_db
class TestListNotificationsView:
    def url(self) -> str:
        return reverse("emails:notifications-list")

    def test_url(self) -> None:
        assert self.url() == "/api/notifications/"

    def setup_method(self) -> None:
        Email.objects.all().delete()
        Block.objects.all().delete()
        Notification.objects.all().delete()

    def test_list_notification_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        url: str = self.url()
        response: Response = client.get(url)
        assert response.status_code == 401

    def test_list_notification_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_notification_fails_with_verified_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_notification_works_with_admin(
        self, client: APIClient
    ) -> None:
        user: User = AdminFaker()
        notification: Notification = NotificationTestFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 200
        assert notification.id == response.data["results"][0]["id"]


@mark.django_db
class TestRetrieveNotificationsView:
    def url(self, pk: int) -> str:
        return reverse("emails:notifications-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/notifications/1/"

    def setup_method(self) -> None:
        Email.objects.all().delete()
        Block.objects.all().delete()
        Notification.objects.all().delete()

    def test_retrieve_notification_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        notification: Notification = NotificationTestFaker()
        url: str = self.url(notification.id)
        response: Response = client.get(url)
        assert response.status_code == 401

    def test_retrieve_notification_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        notification: Notification = NotificationTestFaker()
        user: User = UserFaker()
        url: str = self.url(notification.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_retrieve_notification_fails_with_verified_user(
        self, client: APIClient
    ) -> None:
        notification: Notification = NotificationTestFaker()
        user: User = VerifiedUserFaker()
        url: str = self.url(notification.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_retrieve_notification_works_with_admin(
        self, client: APIClient
    ) -> None:
        user: User = AdminFaker()
        notification: Notification = NotificationTestFaker()
        url: str = self.url(notification.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 200
        assert notification.id == response.data["id"]


@mark.django_db
class TestCreateNotificationsView:
    def url(self) -> str:
        return reverse("emails:notifications-list")

    def test_url(self) -> None:
        assert self.url() == "/api/notifications/"

    def setup_method(self) -> None:
        Email.objects.all().delete()
        Block.objects.all().delete()
        Notification.objects.all().delete()

    def test_post_notification_fails_as_unauthenticated(
        self, client: APIClient, data: dict
    ) -> None:
        url: str = self.url()
        response: Response = client.post(url, data=data, format="json")
        assert response.status_code == 401

    def test_post_notification_fails_with_user_unverified(
        self, client: APIClient, data: dict
    ) -> None:
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data, format="json")
        assert response.status_code == 403

    def test_post_notification_fails_with_verified_user(
        self, client: APIClient, data: dict
    ) -> None:
        user: User = VerifiedUserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data, format="json")
        assert response.status_code == 403

    def test_post_notification_works_with_admin(
        self, client: APIClient, data: dict
    ) -> None:
        user: User = AdminFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        assert Notification.objects.count() == 0
        assert Block.objects.count() == 0
        response: Response = client.post(url, data=data, format="json")
        assert Notification.objects.count() == 1
        assert Block.objects.count() == 1
        assert Notification.objects.first().blocks.count() == 1
        assert response.status_code == 201


@mark.django_db
class TestUpdateNotificationsView:
    def url(self, pk: int) -> str:
        return reverse("emails:notifications-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/notifications/1/"

    def setup_method(self) -> None:
        Email.objects.all().delete()
        Block.objects.all().delete()
        Notification.objects.all().delete()

    def test_update_notification_fails_as_unauthenticated(
        self, client: APIClient, data: dict
    ) -> None:
        notification: Notification = NotificationTestFaker()
        url: str = self.url(notification.id)
        response: Response = client.put(url, data=data, format="json")
        assert response.status_code == 401

    def test_update_notification_fails_with_user_unverified(
        self, client: APIClient, data: dict
    ) -> None:
        notification: Notification = NotificationTestFaker()
        user: User = UserFaker()
        url: str = self.url(notification.id)
        client.force_authenticate(user=user)
        response: Response = client.put(url, data=data, format="json")
        assert response.status_code == 403

    def test_update_notification_fails_with_verified_user(
        self, client: APIClient, data: dict
    ) -> None:
        notification: Notification = NotificationTestFaker()
        user: User = VerifiedUserFaker()
        client.force_authenticate(user=user)
        url: str = self.url(notification.id)
        response: Response = client.put(url, data=data, format="json")
        assert response.status_code == 403

    def test_update_notification_works_with_admin(
        self, client: APIClient, data: dict
    ) -> None:
        user: User = AdminFaker()
        notification: Notification = NotificationTestFaker()
        url: str = self.url(notification.id)
        client.force_authenticate(user=user)
        response: Response = client.put(url, data=data, format="json")
        assert response.status_code == 200
        assert notification.id == response.data["id"]


@mark.django_db
class TestDeleteNotificationsView:
    def url(self, pk: int) -> str:
        return reverse("emails:notifications-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/notifications/1/"

    def setup_method(self) -> None:
        Email.objects.all().delete()
        Block.objects.all().delete()
        Notification.objects.all().delete()

    def test_delete_notification_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        notification: Notification = NotificationTestFaker()
        url: str = self.url(notification.id)
        response: Response = client.delete(url)
        assert response.status_code == 401

    def test_delete_notification_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        notification: Notification = NotificationTestFaker()
        user: User = UserFaker()
        url: str = self.url(notification.id)
        client.force_authenticate(user=user)
        response: Response = client.delete(url)
        assert response.status_code == 403

    def test_delete_notification_fails_with_verified_user(
        self, client: APIClient
    ) -> None:
        notification: Notification = NotificationTestFaker()
        user: User = VerifiedUserFaker()
        url: str = self.url(notification.id)
        client.force_authenticate(user=user)
        response: Response = client.delete(url)
        assert response.status_code == 403

    def test_delete_notification_works_with_admin(
        self, client: APIClient
    ) -> None:
        user: User = AdminFaker()
        notification: Notification = NotificationTestFaker()
        url: str = self.url(notification.id)
        client.force_authenticate(user=user)
        assert Notification.objects.count() == 1
        response: Response = client.delete(url)
        assert response.status_code == 204
        assert Notification.objects.count() == 0
