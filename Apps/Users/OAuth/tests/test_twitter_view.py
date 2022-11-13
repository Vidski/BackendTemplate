import pytest
from django.conf import settings
from django.urls import reverse
from mock import PropertyMock
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
class TestTwitterAuthView:
    def url(self) -> str:
        return reverse("oauth:twitter")

    def test_url(self) -> None:
        assert self.url() == "/api/oauth/twitter/"

    @patch("twitter.Api.VerifyCredentials")
    def test_twitter_view_creates_new_user(
        self, VerifyCredentials: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        twitter_user: MagicMock = MagicMock()
        name: PropertyMock = PropertyMock(return_value="Test")
        user_email: PropertyMock = PropertyMock(return_value=email)
        type(twitter_user).name = name
        type(twitter_user).email = user_email
        VerifyCredentials.return_value = twitter_user
        assert not User.objects.filter(email=email).exists()
        response: Response = client.post(
            self.url(),
            {
                "access_token_key": "access_token_key",
                "access_token_secret": "access_token_secret",
            },
        )
        assert response.status_code == 200
        assert User.objects.filter(email=email).exists()

    @patch("twitter.Api.VerifyCredentials")
    def test_twitter_view_returns_user_login_data(
        self, VerifyCredentials: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        UserFaker(email=email)
        twitter_user: MagicMock = MagicMock()
        name: PropertyMock = PropertyMock(return_value="Test")
        user_email: PropertyMock = PropertyMock(return_value=email)
        type(twitter_user).name = name
        type(twitter_user).email = user_email
        VerifyCredentials.return_value = twitter_user
        assert User.objects.filter(email=email).exists()
        response: Response = client.post(
            self.url(),
            {
                "access_token_key": "access_token_key",
                "access_token_secret": "access_token_secret",
            },
        )
        assert response.status_code == 200
        assert User.objects.filter(email=email).exists()

    @patch("twitter.Api.VerifyCredentials")
    def test_twitter_view_creates_new_user_with_custom_language(
        self, VerifyCredentials: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        twitter_user: MagicMock = MagicMock()
        name: PropertyMock = PropertyMock(return_value="Test")
        user_email: PropertyMock = PropertyMock(return_value=email)
        type(twitter_user).name = name
        type(twitter_user).email = user_email
        VerifyCredentials.return_value = twitter_user
        assert not User.objects.filter(email=email).exists()
        data: dict = {
            "access_token_key": "access_token_key",
            "access_token_secret": "access_token_secret",
            "preferred_language": "ES",
        }
        assert User.objects.count() == 0
        response: Response = client.post(
            self.url(),
            data,
        )
        assert response.status_code == 200
        assert User.objects.filter(email=email).exists()
        assert User.objects.first().preferred_language == "ES"

    @patch("twitter.Api.VerifyCredentials")
    def test_twitter_view_creates_new_user_with_default_language_if_not_passed(
        self, VerifyCredentials: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        twitter_user: MagicMock = MagicMock()
        name: PropertyMock = PropertyMock(return_value="Test")
        user_email: PropertyMock = PropertyMock(return_value=email)
        type(twitter_user).name = name
        type(twitter_user).email = user_email
        VerifyCredentials.return_value = twitter_user
        assert not User.objects.filter(email=email).exists()
        data: dict = {
            "access_token_key": "access_token_key",
            "access_token_secret": "access_token_secret",
        }
        assert User.objects.count() == 0
        response: Response = client.post(
            self.url(),
            data,
        )
        assert response.status_code == 200
        assert User.objects.filter(email=email).exists()
        assert User.objects.first().preferred_language == "EN"

    @patch("twitter.Api.VerifyCredentials")
    def test_twitter_view_creates_new_user_with_default_language_if_wrong_passed(
        self, VerifyCredentials: MagicMock, client: APIClient
    ) -> None:
        email: str = "test@test.com"
        twitter_user: MagicMock = MagicMock()
        name: PropertyMock = PropertyMock(return_value="Test")
        user_email: PropertyMock = PropertyMock(return_value=email)
        type(twitter_user).name = name
        type(twitter_user).email = user_email
        VerifyCredentials.return_value = twitter_user
        assert not User.objects.filter(email=email).exists()
        data: dict = {
            "access_token_key": "access_token_key",
            "access_token_secret": "access_token_secret",
            "preferred_language": "WRONG",
        }
        assert User.objects.count() == 0
        response: Response = client.post(
            self.url(),
            data,
        )
        assert response.status_code == 200
        assert User.objects.filter(email=email).exists()
        assert User.objects.first().preferred_language == "EN"
