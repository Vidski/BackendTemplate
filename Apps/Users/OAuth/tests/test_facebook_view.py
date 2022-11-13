import pytest
from django.conf import settings
from django.urls import reverse
from mock import patch
from mock.mock import MagicMock
from rest_framework.response import Response
from rest_framework.test import APIClient

from Users.fakers.user import UserFaker
from Users.models import User


@pytest.fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestFacebookAuthView:
    def url(self) -> str:
        return reverse("oauth:facebook")

    def test_url(self) -> None:
        assert self.url() == "/api/oauth/facebook/"

    @patch("facebook.GraphAPI.request")
    def test_facebook_view_creates_new_user(
        self, request: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        request.return_value = {
            "email": email,
            "first_name": "Test",
            "last_name": "Test",
        }
        assert not User.objects.filter(email=email).exists()
        response: Response = client.post(self.url(), {"token": "token"})
        assert response.status_code == 200
        assert User.objects.filter(email=email).exists()

    @patch("facebook.GraphAPI.request")
    def test_facebook_view_returns_user_login_data(
        self, request: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        UserFaker(email=email)
        request.return_value = {
            "email": email,
            "first_name": "Test",
            "last_name": "Test",
        }
        response: Response = client.post(self.url(), {"token": "token"})
        assert response.status_code == 200

    @patch("facebook.GraphAPI.request")
    def test_facebook_view_creates_new_user_with_custom_language(
        self, request: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        request.return_value = {
            "email": email,
            "first_name": "Test",
            "last_name": "Test",
        }
        assert not User.objects.filter(email=email).exists()
        data: dict = {
            "token": "token",
            "preferred_language": "ES",
        }
        assert User.objects.count() == 0
        response: Response = client.post(self.url(), data)
        assert response.status_code == 200
        assert User.objects.count() == 1
        assert User.objects.filter(email=email).exists()
        assert User.objects.first().preferred_language == "ES"

    @patch("facebook.GraphAPI.request")
    def test_facebook_view_creates_new_user_with_default_language_if_not_passed(
        self, request: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        request.return_value = {
            "email": email,
            "first_name": "Test",
            "last_name": "Test",
        }
        assert not User.objects.filter(email=email).exists()
        data: dict = {
            "token": "token",
        }
        assert User.objects.count() == 0
        response: Response = client.post(self.url(), data)
        assert response.status_code == 200
        assert User.objects.count() == 1
        assert User.objects.filter(email=email).exists()
        assert User.objects.first().preferred_language == "EN"

    @patch("facebook.GraphAPI.request")
    def test_facebook_view_creates_new_user_with_default_language_if_wrong_passed(
        self, request: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        request.return_value = {
            "email": email,
            "first_name": "Test",
            "last_name": "Test",
        }
        assert not User.objects.filter(email=email).exists()
        data: dict = {
            "token": "token",
            "preferred_language": "WRONG",
        }
        assert User.objects.count() == 0
        response: Response = client.post(self.url(), data)
        assert response.status_code == 200
        assert User.objects.count() == 1
        assert User.objects.filter(email=email).exists()
        assert User.objects.first().preferred_language == "EN"
