import json

import pytest
from django.core import mail
from rest_framework.response import Response
from rest_framework.test import APIClient

from Users.factories.user import UserFactory
from Users.fakers.user import VerifiedUserFaker
from Users.models import User


ENDPOINT: str = "/api/auth"


@pytest.fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestUserSignUpEndpoint:
    def test_create_user_fails_with_an_used_email(
        self, client: APIClient
    ) -> None:
        UserFactory(email="emailused@appname.me")
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailused@appname.me",
            "password": "password",
            "password_confirmation": "password",
        }
        response: Response = client.post(
            f"{ENDPOINT}/signup/", data, format="json"
        )
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
        response: Response = client.post(
            f"{ENDPOINT}/signup/", data, format="json"
        )
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
        response: Response = client.post(
            f"{ENDPOINT}/signup/", data, format="json"
        )
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
        # Normal and admin user already in database
        assert User.objects.count() == 0
        response: Response = client.post(
            f"{ENDPOINT}/signup/", data, format="json"
        )
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


@pytest.mark.django_db
class TestUserLogInEndpoint:
    def test_login_fails_with_wrong_email(self, client: APIClient) -> None:
        data: dict = {
            "email": "wroongemail@appname.me",
            "password": "RightPassword",
        }
        response: Response = client.post(
            f"{ENDPOINT}/login/", data, format="json"
        )
        message: str = "Invalid credentials"
        assert response.status_code == 400
        assert message in response.data

    def test_login_fails_with_wrong_password(self, client: APIClient) -> None:
        UserFactory(email="rightemail@appname.me", password="RightPassword")
        data: dict = {
            "email": "rightemail@appname.me",
            "password": "WrongPassword",
        }
        response: Response = client.post(
            f"{ENDPOINT}/login/", data, format="json"
        )
        message: str = "Invalid credentials"
        assert response.status_code == 400
        assert message in response.data

    def test_login_fails_with_user_not_verified(
        self, client: APIClient
    ) -> None:
        UserFactory(email="rightemail@appname.me", password="RightPassword")
        data: dict = {
            "email": "rightemail@appname.me",
            "password": "RightPassword",
        }
        response: Response = client.post(
            f"{ENDPOINT}/login/", data, format="json"
        )
        message: str = "User is not verified"
        assert response.status_code == 400
        assert message in response.data

    def test_log_in_is_successful_with_a_verified_user(
        self, client: APIClient
    ) -> None:
        testing_user: User = VerifiedUserFaker(
            email="rightemail@appname.me", password="RightPassword"
        )
        data: dict = {
            "email": "rightemail@appname.me",
            "password": "RightPassword",
        }
        response: Response = client.post(
            f"{ENDPOINT}/login/", data, format="json"
        )
        assert response.status_code == 200
        data: dict = json.loads(response.content)
        assert "token" in data
        assert "refresh_token" in data
        assert data["first_name"] == testing_user.first_name
        assert data["last_name"] == testing_user.last_name
        assert data["email"] == testing_user.email
