import pytest
from mock import patch
from mock.mock import MagicMock
from rest_framework.serializers import ValidationError

from SocialAuth.serializers import FacebookOAuthSerializer


@pytest.mark.django_db
class TestFacebookOAuthSerializer:
    @patch("facebook.GraphAPI.request")
    def test_validate_token_do_not_raises_an_error(
        self, request: MagicMock
    ) -> None:
        request.return_value = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "Test",
        }
        token: str = "token"
        serializer: FacebookOAuthSerializer = FacebookOAuthSerializer()
        serializer.validate_token(token)
        request.assert_called_once()

    def test_validate_token_do_raises_an_error(self) -> None:
        token: str = "token"
        serializer: FacebookOAuthSerializer = FacebookOAuthSerializer()
        with pytest.raises(ValidationError):
            serializer.validate_token(token)
