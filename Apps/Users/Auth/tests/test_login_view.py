import json

import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import User


@pytest.fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestUserLogInEndpoint:
    def url(self) -> str:
        return reverse("auth:auth-login")

    def test_url(self) -> None:
        assert self.url() == "/api/auth/login/"

    def test_login_fails_with_wrong_email(self, client: APIClient) -> None:
        data: dict = {
            "email": "wroongemail@appname.me",
            "password": "RightPassword",
        }
        response: Response = client.post(self.url(), data, format="json")
        message: str = "Invalid credentials"
        assert response.status_code == 400
        assert message in response.data

    def test_login_fails_with_wrong_password(self, client: APIClient) -> None:
        UserFaker(email="rightemail@appname.me", password="RightPassword")
        data: dict = {
            "email": "rightemail@appname.me",
            "password": "WrongPassword",
        }
        response: Response = client.post(self.url(), data, format="json")
        message: str = "Invalid credentials"
        assert response.status_code == 400
        assert message in response.data

    def test_login_fails_with_user_not_verified(
        self, client: APIClient
    ) -> None:
        UserFaker(email="rightemail@appname.me", password="RightPassword")
        data: dict = {
            "email": "rightemail@appname.me",
            "password": "RightPassword",
        }
        response: Response = client.post(self.url(), data, format="json")
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
        response: Response = client.post(self.url(), data, format="json")
        assert response.status_code == 200
        data: dict = json.loads(response.content)
        assert "token" in data
        assert "refresh_token" in data
        assert data["first_name"] == testing_user.first_name
        assert data["last_name"] == testing_user.last_name
        assert data["email"] == testing_user.email
