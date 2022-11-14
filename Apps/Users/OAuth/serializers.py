from django.conf import settings
from facebook import GraphAPI
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import CharField
from rest_framework.serializers import Serializer
from rest_framework.serializers import ValidationError
from twitter import Api
from twitter import User as TwitterUser

from Users.choices import PreferredLanguageChoices
from Users.OAuth.user_handler import RegisterOrLoginViaFacebook
from Users.OAuth.user_handler import RegisterOrLoginViaGoogle
from Users.OAuth.user_handler import RegisterOrLoginViaTwitter


class BaseSerializer(Serializer):
    def get_base_data(self) -> dict:
        language: str = self.get_initial().get("preferred_language", None)
        if not language or language not in PreferredLanguageChoices.values:
            language = PreferredLanguageChoices.ENGLISH
        return {"preferred_language": language}


class GoogleOAuthSerializer(BaseSerializer):
    token: CharField = CharField()
    preferred_language: CharField = CharField(required=False)

    def validate_token(self, token: str) -> bool:
        user_data: dict = self.get_user_data(token)
        self.validate_aud(user_data["aud"])
        self._data: dict = RegisterOrLoginViaGoogle(user_data).serialized_user
        return True

    def get_user_data(self, token: str) -> dict:
        try:
            return {
                **self.get_base_data(),
                **verify_oauth2_token(token, Request()),
            }
        except:
            raise ValidationError("Token is invalid or expired. Try again.")

    def validate_aud(self, aud: str) -> None:
        if aud != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("Google client id is invalid")


class FacebookOAuthSerializer(BaseSerializer):
    token: CharField = CharField()
    preferred_language = CharField(required=False)

    def validate_token(self, token: str) -> bool:
        user_data = self.get_user_data(token)
        self._data: dict = RegisterOrLoginViaFacebook(user_data).serialized_user
        return True

    def get_user_data(self, token: str) -> dict:
        try:
            graph: GraphAPI = GraphAPI(access_token=token)
            graph_query: str = "/me?fields=first_name,last_name,email"
            return {**self.get_base_data(), **graph.request(graph_query)}
        except:
            raise ValidationError("Token is invalid or expired. Try again.")


class TwitterOAuthSerializer(BaseSerializer):
    access_token_key: CharField = CharField()
    access_token_secret: CharField = CharField()
    preferred_language: CharField = CharField(required=False)

    def validate(self, attributes: dict) -> bool:
        twitter_user: TwitterUser = self.get_user_data(attributes)
        user_data: dict = self.get_dictionary_of_user_data(twitter_user)
        self._data: dict = RegisterOrLoginViaTwitter(user_data).serialized_user
        return True

    def get_user_data(self, attributes: dict) -> TwitterUser:
        try:
            api: Api = self.get_twitter_api(attributes)
            return api.VerifyCredentials(include_email=True)
        except Exception:
            raise ValidationError("Token is invalid or expired. Try again.")

    def get_dictionary_of_user_data(self, user: TwitterUser) -> dict:
        if not getattr(user, "email", None):
            raise ValidationError("Email is not available and is required.")
        return {
            **self.get_base_data(),
            "email": getattr(user, "email"),
            "name": getattr(user, "name", None),
        }

    def get_twitter_api(self, attributes: dict) -> Api:
        return Api(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET_KEY,
            access_token_key=attributes.get("access_token_key", None),
            access_token_secret=attributes.get("access_token_secret", None),
        )
