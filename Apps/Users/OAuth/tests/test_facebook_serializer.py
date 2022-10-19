import pytest
from mock import patch
from mock.mock import MagicMock
from rest_framework.serializers import ValidationError

from Users.Auth.serializers import UserAuthSerializer
from Users.models import User
from Users.OAuth.serializers import FacebookOAuthSerializer


@pytest.mark.django_db
class TestFacebookOAuthSerializer:
    @patch("facebook.GraphAPI.request")
    def test_validate_token_returns_user_data(self, request: MagicMock) -> None:
        request.return_value = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "Test",
        }
        token: str = "token"
        serializer: FacebookOAuthSerializer = FacebookOAuthSerializer()
        serializer.validate_token(token)
        data: dict = serializer.data
        del data["token"]
        del data["refresh_token"]
        request.assert_called_once()
        user: User = User.objects.get(email="test@test.com")
        expected_data: dict = UserAuthSerializer(user).data
        del expected_data["token"]
        del expected_data["refresh_token"]
        assert data == expected_data

    def test_validate_token_raises_an_error(self) -> None:
        token: str = "token"
        serializer: FacebookOAuthSerializer = FacebookOAuthSerializer()
        with pytest.raises(ValidationError):
            serializer.validate_token(token)
