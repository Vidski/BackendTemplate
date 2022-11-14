from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Emails.fakers.email import EmailTestFaker
from Emails.models import Email
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import User


@fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@mark.django_db
class TestListEmailsView:
    def url(self) -> str:
        return reverse("emails:emails-list")

    def test_url(self) -> None:
        assert self.url() == "/api/emails/"

    def test_list_emails_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        url: str = self.url()
        response: Response = client.get(url)
        assert response.status_code == 401

    def test_list_emails_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_emails_fails_with_user(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_emails_works_with_admin(self, client: APIClient) -> None:
        url: str = self.url()
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        response: Response = client.get(url)
        assert response.status_code == 200


@mark.django_db
class TestRetrieveEmailsView:
    def url(self, pk: int) -> str:
        return reverse("emails:emails-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/emails/1/"

    def test_retrieve_email_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        response: Response = client.get(url)
        assert response.status_code == 401

    def test_retrieve_email_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_retrieve_email_fails_with_user(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_retrieve_email_works_with_admin(self, client: APIClient) -> None:
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        response: Response = client.get(url)
        assert response.status_code == 200


@mark.django_db
class TestCreateEmailsView:
    def url(self) -> str:
        return reverse("emails:emails-list")

    def test_url(self) -> None:
        assert self.url() == "/api/emails/"

    def test_post_email_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        data: dict = {
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
        url: str = self.url()
        response: Response = client.post(url, data=data, format="json")
        assert response.status_code == 401

    def test_post_email_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        data: dict = {
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
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data, format="json")
        assert response.status_code == 403

    def test_post_email_fails_with_user(self, client: APIClient) -> None:
        data: dict = {
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
        user: User = VerifiedUserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data, format="json")
        assert response.status_code == 403

    def test_post_email_works_with_admin(self, client: APIClient) -> None:
        user: User = UserFaker()
        data: dict = {
            "header": "Email header",
            "affair": "NOTIFICATION",
            "subject": "Email subject",
            "to": f"{user.email}",
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
        url: str = self.url()
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        assert Email.objects.count() == 0
        response: Response = client.post(url, data=data, format="json")
        assert response.status_code == 201
        assert Email.objects.count() == 1

    def test_post_email_works_fails_due_bad_block_data(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        data: dict = {
            "header": "Email header",
            "affair": "NOTIFICATION",
            "subject": "Email subject",
            "to": f"{user.email}",
            "is_test": True,
            "programed_send_date": "2050-12-12T10:59.000",
            "blocks": [
                {
                    "title": "Block title",
                    "content": "Block content",
                    "link_text": "Click here",
                    "show_link": "INVALID TYPE HERE",
                    "link": "google.com",
                }
            ],
        }
        url: str = self.url()
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        assert Email.objects.count() == 0
        response: Response = client.post(url, data=data, format="json")
        assert response.status_code == 400
        assert Email.objects.count() == 0


@mark.django_db
class TestUpdateEmailsView:
    def url(self, pk: int) -> str:
        return reverse("emails:emails-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/emails/1/"

    def test_update_email_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        data: dict = {
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
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        response: Response = client.put(url, data=data, format="json")
        assert response.status_code == 401

    def test_update_email_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        data: dict = {
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
        user: User = UserFaker()
        client.force_authenticate(user=user)
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        response: Response = client.put(url, data=data, format="json")
        assert response.status_code == 403

    def test_update_email_fails_with_user(self, client: APIClient) -> None:
        data: dict = {
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
        user: User = VerifiedUserFaker()
        client.force_authenticate(user=user)
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        response: Response = client.put(url, data=data, format="json")
        assert response.status_code == 403

    def test_update_email_works_with_admin(self, client: APIClient) -> None:
        user: User = UserFaker()
        data: dict = {
            "header": "Email header",
            "affair": "NOTIFICATION",
            "subject": "Email subject",
            "to": f"{user.email}",
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
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        assert Email.objects.count() == 0
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        response: Response = client.put(url, data=data, format="json")
        assert response.status_code == 200
        assert Email.objects.count() == 1


@mark.django_db
class TestDeleteEmailsView:
    def url(self, pk: int) -> str:
        return reverse("emails:emails-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/emails/1/"

    def test_delete_email_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        response: Response = client.delete(url)
        assert response.status_code == 401

    def test_delete_email_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        client.force_authenticate(user=user)
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        response: Response = client.delete(url)
        assert response.status_code == 403

    def test_delete_email_fails_with_user(self, client: APIClient) -> None:
        user: User = VerifiedUserFaker()
        client.force_authenticate(user=user)
        email: Email = EmailTestFaker()
        url: str = self.url(email.id)
        response: Response = client.delete(url)
        assert response.status_code == 403

    def test_delete_email_works_with_admin(self, client: APIClient) -> None:
        user: User = UserFaker()
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        email: Email = EmailTestFaker()
        assert Email.objects.count() == 1
        url: str = self.url(email.id)
        response: Response = client.delete(url)
        assert response.status_code == 204
        assert Email.objects.count() == 0
