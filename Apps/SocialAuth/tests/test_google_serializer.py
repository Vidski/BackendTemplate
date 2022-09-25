import pytest
from django.conf import settings
from mock import patch
from mock.mock import MagicMock
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ValidationError

from SocialAuth.serializers import GoogleOAuthSerializer
from Users.models import User
from Users.serializers import UserSignUpSerializer


@pytest.mark.django_db
class TestGoogleOAuthSerializer:
    @patch("SocialAuth.serializers.verify_oauth2_token")
    def test_validate_token_returns_user_data(
        self, mock_verify_oauth2_token: MagicMock
    ) -> None:
        mock_verify_oauth2_token.return_value = {
            "email": "test@test.com",
            "given_name": "Test",
            "family_name": "Test",
            "aud": settings.GOOGLE_CLIENT_ID,
        }
        token: str = "token"
        serializer: GoogleOAuthSerializer = GoogleOAuthSerializer()
        data: dict = serializer.validate_token(token)
        mock_verify_oauth2_token.assert_called_once()
        user: User = User.objects.get(email="test@test.com")
        assert data == UserSignUpSerializer(user).data

    def test_validate_token_do_raises_an_error(self) -> None:
        token: str = "token"
        serializer: GoogleOAuthSerializer = GoogleOAuthSerializer()
        with pytest.raises(ValidationError):
            serializer.validate_token(token)

    @patch("SocialAuth.serializers.verify_oauth2_token")
    def test_validate_aud_do_raises_an_error(
        self, mock_verify_oauth2_token: MagicMock
    ) -> None:
        mock_verify_oauth2_token.return_value = {
            "email": "test@test.com",
            "given_name": "Test",
            "family_name": "Test",
            "aud": "invalid",
        }
        token: str = "token"
        serializer: GoogleOAuthSerializer = GoogleOAuthSerializer()
        with pytest.raises(AuthenticationFailed):
            serializer.validate_token(token)
