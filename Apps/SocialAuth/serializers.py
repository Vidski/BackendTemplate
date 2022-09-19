from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import CharField
from rest_framework.serializers import Serializer
from rest_framework.serializers import ValidationError

from SocialAuth.user_handler import RegisterOrLogin


class GoogleOAuthSerializer(Serializer):
    token: CharField = CharField()

    def validate_token(self, token: str) -> dict:
        user_data: dict = self.get_user_data(token)
        self.validate_aud(user_data["aud"])
        return RegisterOrLogin("google", user_data).serialized_user

    def get_user_data(self, token: str) -> dict:
        try:
            return verify_oauth2_token(token, Request())
        except:
            raise ValidationError("Token is invalid or expired. Try again.")

    def validate_aud(self, aud: str) -> None:
        if aud != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("Google client id is invalid")
