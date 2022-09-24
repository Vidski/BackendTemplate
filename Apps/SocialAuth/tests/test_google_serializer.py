import pytest
from django.conf import settings
from mock import patch
from mock.mock import MagicMock
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ValidationError

from SocialAuth.serializers import GoogleOAuthSerializer


@pytest.mark.django_db
class TestGoogleOAuthSerializer:
    @patch("SocialAuth.serializers.verify_oauth2_token")
    def test_validate_token_do_not_raises_an_error(
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
        serializer.validate_token(token)
        mock_verify_oauth2_token.assert_called_once()

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
