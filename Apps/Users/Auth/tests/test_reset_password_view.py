import pytest
from django.core import mail
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework.response import Response
from rest_framework.test import APIClient

from Users.fakers.user import UserFaker
from Users.models import User


@pytest.mark.django_db
class TestUserPasswordResetTests:
    def test_reset_password(self, client: APIClient) -> None:
        # Test that any user can reset its password via API
        normal_user: User = UserFaker()
        assert normal_user.check_password("password") is True
        response: Response = client.post(
            f"/api/reset_password/", {"email": normal_user.email}
        )
        assert response.status_code == 200
        tokens: ResetPasswordToken = ResetPasswordToken.objects.all()
        assert len(tokens) == 1
        token: int = tokens[0].key
        data: dict = {"token": token, "password": "NewPassword95"}
        client.post(f"/api/reset_password/confirm/", data, format="json")
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.check_password("NewPassword95") is True
        assert len(mail.outbox) == 1
