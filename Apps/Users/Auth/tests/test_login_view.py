import json

import pytest
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
