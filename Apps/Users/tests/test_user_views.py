from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import Profile
from Users.models import User
from Users.utils import generate_user_verification_token


@fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@mark.django_db
class TestUserListEndpoint:
    def url(self) -> str:
        return reverse("users:users-list")

    def test_url(self) -> None:
        assert self.url() == "/api/users/"

    def test_list_users_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        response: Response = client.get(self.url(), format="json")
        assert response.status_code == 401

    def test_list_users_fails_as_an_authenticated_unverified_normal_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(self.url(), format="json")
        assert response.status_code == 403

    def test_list_users_fails_as_an_authenticated_verified_normal_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(self.url(), format="json")
        assert response.status_code == 403

    def test_list_users_is_successful_as_an_admin_user(
        self, client: APIClient
    ) -> None:
        admin_user: User = AdminFaker()
        client.force_authenticate(user=admin_user)
        response: Response = client.get(self.url(), format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_list_users_is_successful_as_an_admin_user_paginating(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        admin_user: User = AdminFaker()
        client.force_authenticate(user=admin_user)
        url: str = f"{self.url()}?page=1&page_size=1"
        response: Response = client.get(url, format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        admin_name = admin_user.first_name
        assert response.data["results"][0]["first_name"] == admin_name
        url: str = f"{self.url()}?page=2&page_size=1"
        response: Response = client.get(url, format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        admin_name = user.first_name
        assert response.data["results"][0]["first_name"] == admin_name


@mark.django_db
class TestUserRetrieveEndpoint:
    def url(self, pk: int = None) -> str:
        return reverse("users:users-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/users/1/"

    def test_get_user_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        response: Response = client.get(self.url(normal_user.id), format="json")
        assert response.status_code == 401

    def test_get_user_fails_as_an_authenticated_unverified_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(self.url(normal_user.id), format="json")
        assert response.status_code == 403

    def test_get_user_fails_as_an_authenticated_verified_user_to_other_users_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(self.url(admin_user.id), format="json")
        assert response.status_code == 403

    def test_get_user_is_successful_as_an_authenticated_verified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(self.url(normal_user.id), format="json")
        assert response.status_code == 200
        assert response.data["id"] == normal_user.id
        assert response.data["email"] == normal_user.email

    def test_get_user_is_successful_to_other_users_data_as_admin(
        self, client: APIClient
    ) -> None:
        admin_user: User = AdminFaker()
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=admin_user)
        response: Response = client.get(self.url(normal_user.id), format="json")
        assert response.status_code == 200


@mark.django_db
class TestUserUpdateEndpoint:
    def url(self, pk: int = None) -> str:
        return reverse("users:users-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/users/1/"

    def test_update_user_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test edited",
            "last_name": "Tested Edit",
            "email": "edituser2@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "NewPassword95",
        }
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 401

    def test_update_user_fails_as_an_authenticated_unverified_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        data: dict = {
            "first_name": "Test edited",
            "last_name": "Tested Edit",
            "email": "edituser2@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "NewPassword95",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 403

    def test_update_user_fails_as_an_authenticated_verified_user_to_other_users_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        data: dict = {
            "first_name": "Test edited",
            "last_name": "Tested Edit",
            "email": "edituser2@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "NewPassword95",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            self.url(admin_user.id), data, format="json"
        )
        assert response.status_code == 403
        assert normal_user.email != data["email"]

    def test_update_user_is_successful_as_an_authenticated_verified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test edited",
            "last_name": "Tested Edit",
            "email": "edituser2@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "NewPassword95",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.email == data["email"]
        assert normal_user.phone_number == data["phone_number"]
        assert normal_user.first_name == data["first_name"]
        assert normal_user.last_name == data["last_name"]
        assert normal_user.check_password(data["password"]) is True

    def test_update_user_fails_as_an_authenticated_verified_user_with_an_used_email(
        self, client: APIClient
    ) -> None:
        UserFaker(email="emailused@appname.me")
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailused@appname.me",
            "password": "password",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 400
        assert "Email is taken" in response.data["email"]

    def test_update_user_fails_as_an_authenticated_verified_user_with_an_used_phone_number(
        self, client: APIClient
    ) -> None:
        UserFaker(phone_number="+13999999999")
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "edituser3@appname.me",
            "password": "password",
            "phone_number": "+13999999999",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 400
        assert "Phone number is taken" in response.data["phone_number"]

    def test_update_user_fails_as_an_authenticated_verified_user_with_a_wrong_old_password(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "finalemail@appname.me",
            "phone_number": "+32987654321",
            "old_password": "NewPassword95 wrong",
            "password": "This is a password",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        message: str = "Wrong password"
        assert response.status_code == 400
        assert message in response.data["password"]

    def test_update_user_fails_as_an_authenticated_verified_user_without_old_password(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "finalemail@appname.me",
            "phone_number": "+32987654321",
            "password": "This is a password",
        }
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        message: str = "Old password is required"
        assert response.status_code == 400
        assert message in response.data["password"]

    def test_update_user_is_successful_as_an_authenticated_verified_user_with_just_a_new_password(
        self, client: APIClient
    ) -> None:
        data: dict = {"old_password": "password", "password": "New Password"}
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.check_password(data["password"]) is True

    def test_update_user_is_successful_as_an_authenticated_verified_user_but_do_not_change_special_fields(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailemail@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "New password",
            "is_verified": False,
            "is_admin": True,
            "is_premium": True,
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.email == data["email"]
        assert normal_user.phone_number == data["phone_number"]
        assert normal_user.first_name == data["first_name"]
        assert normal_user.last_name == data["last_name"]
        assert normal_user.check_password(data["password"]) is True
        assert normal_user.is_verified is True
        assert normal_user.is_admin is False
        assert normal_user.is_premium is False

    def test_update_user_is_successful_as_admin_to_other_user_data_but_do_not_change_special_fields(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailemail@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "New password",
            "is_verified": False,
            "is_admin": True,
            "is_premium": True,
        }
        client.force_authenticate(user=admin_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.email == data["email"]
        assert normal_user.phone_number == data["phone_number"]
        assert normal_user.first_name == data["first_name"]
        assert normal_user.last_name == data["last_name"]
        assert normal_user.check_password(data["password"]) is True
        assert normal_user.is_verified is True
        assert normal_user.is_admin is False
        assert normal_user.is_premium is False

    def test_update_user_fails_with_wrong_phone_format(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailemail@appname.me",
            "phone_number": "32987654321",
            "old_password": "password",
            "password": "New password",
            "is_verified": False,
            "is_admin": True,
            "is_premium": True,
        }
        client.force_authenticate(user=admin_user)
        response: Response = client.put(
            self.url(normal_user.id), data, format="json"
        )
        assert response.status_code == 400


@mark.django_db
class TestUserDeleteEndpoint:
    def url(self, pk: int = None) -> str:
        return reverse("users:users-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/users/1/"

    def test_delete_user_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        assert User.objects.count() == 1
        response: Response = client.delete(
            self.url(normal_user.id), format="json"
        )
        assert response.status_code == 401
        assert User.objects.count() == 1

    def test_delete_user_fails_as_an_authenticated_unverified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.delete(
            self.url(normal_user.id), format="json"
        )
        assert response.status_code == 403
        assert User.objects.count() == 1

    def test_delete_user_fails_as_an_authenticated_verified_user_to_to_other_users_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        admin_user: User = AdminFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.delete(
            self.url(admin_user.id), format="json"
        )
        assert response.status_code == 403
        assert User.objects.count() == 2

    def test_delete_user_is_successful_as_an_authenticated_verified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.delete(
            self.url(normal_user.id), format="json"
        )
        assert response.status_code == 204
        assert User.objects.count() == 0

    def test_delete_user_is_successful_as_admin_to_other_users_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        client.force_authenticate(user=admin_user)
        response: Response = client.delete(
            self.url(normal_user.id), format="json"
        )
        assert response.status_code == 204
        assert User.objects.count() == 1


@mark.django_db
class TestUserVerifyEndpoint:
    def url(self, pk: int = None, token: str = None) -> str:
        return f"{reverse('users:users-verify', args=[pk])}?token={token}"

    def test_url(self) -> None:
        assert self.url(1, "token") == "/api/users/1/verify/?token=token"

    def test_verify_user(self, client: APIClient) -> None:
        # Test that any user can verify its user with a get
        # request with it id and token
        normal_user: User = UserFaker()
        token = generate_user_verification_token(normal_user)
        assert normal_user.is_verified is False
        response: Response = client.get(self.url(normal_user.id, token))
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.is_verified is True
