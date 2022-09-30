import pytest
from mock import PropertyMock
from mock import patch
from mock.mock import MagicMock
from rest_framework.serializers import ValidationError

from Users.Auth.serializers import UserAuthSerializer
from Users.models import User
from Users.OAuth.serializers import TwitterOAuthSerializer


@pytest.mark.django_db
class TestTwitterOAuthSerializer:
    @patch("twitter.Api.VerifyCredentials")
    def test_validate_token_returns_user_data(
        self, VerifyCredentials: MagicMock
    ) -> None:
        twitter_user: MagicMock = MagicMock()
        name: PropertyMock = PropertyMock(return_value="Test")
        email: PropertyMock = PropertyMock(return_value="test@test.com")
        type(twitter_user).name = name
        type(twitter_user).email = email
        VerifyCredentials.return_value = twitter_user
        data: dict = {
            "access_token_key": "access_token_key",
            "access_token_secret": "access_token_secret",
        }
        serializer: TwitterOAuthSerializer = TwitterOAuthSerializer()
        serializer.validate(data)
        data: dict = serializer.data
        del data["token"]
        del data["refresh_token"]
        VerifyCredentials.assert_called_once()
        user: User = User.objects.get(email=twitter_user.email)
        expected_data: dict = UserAuthSerializer(user).data
        del expected_data["token"]
        del expected_data["refresh_token"]
        assert data == expected_data

    def test_validate_token_do_raises_an_error(self) -> None:
        data: dict = {
            "access_token_key": "access_token_key",
            "access_token_secret": "access_token_secret",
        }
        serializer: TwitterOAuthSerializer = TwitterOAuthSerializer()
        with pytest.raises(ValidationError):
            serializer.validate(data)

    @patch("twitter.Api.VerifyCredentials")
    def test_validate_token_raises_an_error_due_lack_of_email(
        self, VerifyCredentials: MagicMock
    ) -> None:
        twitter_user: MagicMock = MagicMock()
        name: PropertyMock = PropertyMock(return_value="Test")
        email: PropertyMock = PropertyMock(return_value=None)
        type(twitter_user).name = name
        type(twitter_user).email = email
        VerifyCredentials.return_value = twitter_user
        data: dict = {
            "access_token_key": "access_token_key",
            "access_token_secret": "access_token_secret",
        }
        serializer: TwitterOAuthSerializer = TwitterOAuthSerializer()
        with pytest.raises(ValidationError):
            serializer.validate(data)
