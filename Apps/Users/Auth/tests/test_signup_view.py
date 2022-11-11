import pytest
from django.core import mail
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from Users.fakers.user import UserFaker
from Users.models import User


@pytest.fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestUserSignUpEndpoint:
    def url(self) -> str:
        return reverse("auth:auth-signup")

    def test_url(self) -> None:
        assert self.url() == f"/api/auth/signup/"

    def test_create_user_fails_with_an_used_email(
        self, client: APIClient
    ) -> None:
        UserFaker(email="emailused@appname.me")
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailused@appname.me",
            "password": "password",
            "password_confirmation": "password",
        }
        response: Response = client.post(self.url(), data, format="json")
        message_one: str = "email"
        message_two: str = "This field must be unique"
        assert response.status_code == 400
        assert message_one in response.data
        assert message_two in response.data["email"][0]
        assert len(mail.outbox) == 0

    def test_create_user_fails_with_a_common_password(
        self, client: APIClient
    ) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemail@appname.me",
            "password": "password",
            "password_confirmation": "password",
        }
        response: Response = client.post(self.url(), data, format="json")
        message: str = "This password is too common."
        assert response.status_code == 400
        assert message in response.data["password"][0]
        assert len(mail.outbox) == 0

    def test_create_user_is_successfull(self, client: APIClient) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemail@appname.me",
            "password": "strongpassword",
            "password_confirmation": "strongpassword",
        }
        assert User.objects.count() == 0
        response: Response = client.post(self.url(), data, format="json")
        assert User.objects.count() == 1
        assert response.status_code == 201
        assert response.data["first_name"] == data["first_name"]
        assert response.data["last_name"] == data["last_name"]
        assert response.data["email"] == data["email"]
        assert response.data["phone_number"] == None
        assert response.data["is_verified"] == False
        assert response.data["is_admin"] == False
        assert response.data["is_premium"] == False
        assert len(mail.outbox) == 1

    def test_sign_up_is_successfully_but_do_not_create_an_user_with_special_fields_modified(
        self, client: APIClient
    ) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemail2@appname.me",
            "password": "strongpassword",
            "password_confirmation": "strongpassword",
            "phone_number": "+34612123123",
            "is_verified": True,
            "is_admin": True,
            "is_premium": True,
        }
        assert User.objects.count() == 0
        response: Response = client.post(self.url(), data, format="json")
        assert User.objects.count() == 1
        assert response.status_code == 201
        assert response.data["first_name"] == data["first_name"]
        assert response.data["last_name"] == data["last_name"]
        assert response.data["email"] == data["email"]
        assert response.data["phone_number"] == None
        assert response.data["is_verified"] == False
        assert response.data["is_admin"] == False
        assert response.data["is_premium"] == False
        assert len(mail.outbox) == 1

    def test_sign_up_is_successfully_with_custom_language(
        self, client: APIClient
    ) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemai@appname.me",
            "password": "strong_password",
            "password_confirmation": "strong_password",
            "preferred_language": "ES",
        }
        assert User.objects.count() == 0
        response: Response = client.post(self.url(), data, format="json")
        assert User.objects.count() == 1
        assert response.status_code == 201
        assert User.objects.first().preferred_language == "ES"
        assert len(mail.outbox) == 1

    def test_sign_up_is_successfully_with_default_language_if_not_passed(
        self, client: APIClient
    ) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemai@appname.me",
            "password": "strong_password",
            "password_confirmation": "strong_password",
        }
        assert User.objects.count() == 0
        response: Response = client.post(self.url(), data, format="json")
        assert User.objects.count() == 1
        assert response.status_code == 201
        assert User.objects.first().preferred_language == "EN"
        assert len(mail.outbox) == 1

    def test_sign_up_is_successfully_with_default_language_if_wrong_passed(
        self, client: APIClient
    ) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemai@appname.me",
            "password": "strong_password",
            "password_confirmation": "strong_password",
            "preferred_language": "WR",
        }
        assert User.objects.count() == 0
        response: Response = client.post(self.url(), data, format="json")
        assert User.objects.count() == 1
        assert response.status_code == 201
        assert User.objects.first().preferred_language == "EN"
        assert len(mail.outbox) == 1
