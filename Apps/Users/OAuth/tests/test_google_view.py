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
class TestGoogleAuthView:
    def url(self) -> str:
        return reverse("oauth:google")

    def test_url(self) -> None:
        assert self.url() == "/api/oauth/google/"

    @patch("Users.OAuth.serializers.verify_oauth2_token")
    def test_google_view_creates_new_user(
        self, mock_verify_oauth2_token: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        mock_verify_oauth2_token.return_value = {
            "email": email,
            "given_name": "Test",
            "family_name": "Test",
            "aud": settings.GOOGLE_CLIENT_ID,
        }
        assert not User.objects.filter(email=email).exists()
        response: Response = client.post(self.url(), {"token": "token"})
        assert response.status_code == 200
        assert User.objects.filter(email=email).exists()

    @patch("Users.OAuth.serializers.verify_oauth2_token")
    def test_google_view_returns_user_login_data(
        self, mock_verify_oauth2_token: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        UserFaker(email=email)
        mock_verify_oauth2_token.return_value = {
            "email": email,
            "given_name": "Test",
            "family_name": "Test",
            "aud": settings.GOOGLE_CLIENT_ID,
        }
        response: Response = client.post(self.url(), {"token": "token"})
        assert response.status_code == 200

    @patch("Users.OAuth.serializers.verify_oauth2_token")
    def test_google_view_creates_new_user_with_custom_language(
        self, mock_verify_oauth2_token: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        mock_verify_oauth2_token.return_value = {
            "email": email,
            "given_name": "Test",
            "family_name": "Test",
            "aud": settings.GOOGLE_CLIENT_ID,
        }
        assert User.objects.count() == 0
        data: dict = {
            "token": "token",
            "preferred_language": "ES",
        }
        response: Response = client.post(self.url(), data)
        assert response.status_code == 200
        assert User.objects.count() == 1
        assert User.objects.first().preferred_language == "ES"

    @patch("Users.OAuth.serializers.verify_oauth2_token")
    def test_google_view_creates_new_user_with_default_language_if_not_passed(
        self, mock_verify_oauth2_token: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        mock_verify_oauth2_token.return_value = {
            "email": email,
            "given_name": "Test",
            "family_name": "Test",
            "aud": settings.GOOGLE_CLIENT_ID,
        }
        assert User.objects.count() == 0
        data: dict = {
            "token": "token",
        }
        response: Response = client.post(self.url(), data)
        assert response.status_code == 200
        assert User.objects.count() == 1
        assert User.objects.first().preferred_language == "EN"

    @patch("Users.OAuth.serializers.verify_oauth2_token")
    def test_google_view_creates_new_user_with_default_language_if_wrong_passed(
        self, mock_verify_oauth2_token: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        mock_verify_oauth2_token.return_value = {
            "email": email,
            "given_name": "Test",
            "family_name": "Test",
            "aud": settings.GOOGLE_CLIENT_ID,
        }
        assert User.objects.count() == 0
        data: dict = {
            "token": "token",
            "preferred_language": "WRONG",
        }
        response: Response = client.post(self.url(), data)
        assert response.status_code == 200
        assert User.objects.count() == 1
        assert User.objects.first().preferred_language == "EN"
