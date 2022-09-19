from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token


class Google:
    @staticmethod
    def validate(auth_token: str) -> dict:
        user_info: dict = verify_oauth2_token(auth_token, Request())
        return user_info
