import pytest
from django.core import mail
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from Emails.choices import CommentType
from Emails.factories.blacklist import BlackListFactory
from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.models.models import BlackList
from Emails.models.models import Suggestion
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import User


@pytest.fixture(scope="function")
def client() -> APIClient:
    return APIClient()


BASE_ENDPOINT: str = "/api/suggestions"


@pytest.mark.django_db
class TestSubmitSuggestionViews:

    ACTION: str = "submit"
    ENDPOINT: str = f"{BASE_ENDPOINT}/{ACTION}/"

    def test_suggestion_fails_as_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        assert len(mail.outbox) == 0
        data: dict = {"type": "Error", "content": "Error found"}
        response: Response = client.post(self.ENDPOINT, data, format="json")
        assert response.status_code == 401
        assert len(mail.outbox) == 0

    def test_suggestion_creates_email_as_authenticated_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        email_count: int = Suggestion.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        type: str = CommentType.ERROR.value
        data: dict = {"type": type, "content": "Error found"}
        client.force_authenticate(user=normal_user)
        response: Response = client.post(self.ENDPOINT, data, format="json")
        email_count: Suggestion = Suggestion.objects.all().count()
        expected_header: str = f"ERROR from user with id: {normal_user.id}"
        assert response.status_code == 201
        assert True == response.data["was_sent"]
        assert "ERROR" == response.data["subject"]
        assert expected_header == response.data["header"]
        block = Suggestion.objects.first().blocks.first()
        assert [block.id] == response.data["blocks"]
        assert "Error found" == response.data["content"]
        assert len(mail.outbox) == 1
        assert email_count == 1

    def test_suggestion_fails_as_authenticated_user_because_wrong_type(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        email_count: int = Suggestion.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        data: dict = {"type": "Wrong", "content": "Error found"}
        client.force_authenticate(user=normal_user)
        response: Response = client.post(self.ENDPOINT, data, format="json")
        email_count: Suggestion = Suggestion.objects.all().count()
        expected_error_message: str = "Type not allowed"
        assert response.status_code == 400
        assert expected_error_message in response.data["detail"]
        assert len(mail.outbox) == 0
        assert email_count == 0


@pytest.mark.django_db
class TestReadSuggestionViews:

    ACTION: str = "read"

    def test_read_suggestion_fails_as_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        type: str = CommentType.ERROR.value
        content: str = "Error found"
        suggestion: Suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        pk: int = suggestion.pk
        url: str = f"{BASE_ENDPOINT}/{pk}/{self.ACTION}/"
        response: Response = client.post(url, format="json")
        assert response.status_code == 401

    def test_read_suggestion_fails_as_unverified_user(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        client.force_authenticate(user=user)
        type: str = CommentType.ERROR.value
        content: str = "Error found"
        suggestion: Suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        pk: int = suggestion.pk
        url: str = f"{BASE_ENDPOINT}/{pk}/{self.ACTION}/"
        response: Response = client.post(url, format="json")
        assert response.status_code == 403

    def test_suggestion_is_read_as_admin(self, client: APIClient) -> None:
        user: User = AdminFaker()
        client.force_authenticate(user=user)
        type: str = CommentType.ERROR.value
        content: str = "Error found"
        suggestion: Suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        assert suggestion.was_read == False
        pk: int = suggestion.pk
        url: str = f"{BASE_ENDPOINT}/{pk}/{self.ACTION}/"
        response: Response = client.post(url, format="json")
        assert response.status_code == 200
        suggestion.refresh_from_db()
        assert suggestion.was_read == True


@pytest.mark.django_db
class TestUserSuggestionViews:

    ACTION: str = "user"

    def test_list_user_suggestion_without_user_id_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        response: Response = client.get(f"{BASE_ENDPOINT}/{self.ACTION}/")
        assert response.status_code == 401

    def test_list_user_suggestion_with_user_id_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        response: Response = client.get(
            f"{BASE_ENDPOINT}/{self.ACTION}/?user={user.id}"
        )
        assert response.status_code == 401

    def test_list_user_suggestion_with_user_id_fails_as_other_user(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        client.force_authenticate(user=user)
        other_user: User = UserFaker()
        type: str = CommentType.ERROR.value
        content: str = "Error found"
        SuggestionEmailFactory(type=type, content=content, user=other_user)
        url: str = f"{BASE_ENDPOINT}/{self.ACTION}/?user_id={other_user.id}"
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_user_suggestion_with_user_id_returns_suggestions_as_admin(
        self, client: APIClient
    ) -> None:
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        user: User = UserFaker()
        type: str = CommentType.ERROR.value
        content: str = "Error found"
        SuggestionEmailFactory(type=type, content=content, user=user)
        url: str = f"{BASE_ENDPOINT}/{self.ACTION}/?user_id={user.id}"
        response: Response = client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["count"] == Suggestion.objects.count()

    def test_list_user_suggestion_with_out_user_id_returns_suggestions_as_user(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        client.force_authenticate(user=user)
        type: str = CommentType.ERROR.value
        content: str = "Error found"
        SuggestionEmailFactory(type=type, content=content, user=user)
        url: str = f"{BASE_ENDPOINT}/{self.ACTION}/"
        response: Response = client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["count"] == Suggestion.objects.count()

    def test_list_user_suggestion_with_user_id_returns_suggestions_as_user(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        client.force_authenticate(user=user)
        type: str = CommentType.ERROR.value
        content: str = "Error found"
        SuggestionEmailFactory(type=type, content=content, user=user)
        url: str = f"{BASE_ENDPOINT}/{self.ACTION}/?user_id={user.id}"
        response: Response = client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["count"] == Suggestion.objects.count()


@pytest.mark.django_db
class TestListBlacklistViews:
    def url(self, pk: int = None) -> str:
        if pk:
            return reverse("emails:blacklist-detail", args=[pk])
        return reverse("emails:blacklist-list")

    def test_url(self) -> None:
        assert self.url() == "/api/blacklist/"
        assert self.url(pk=1) == "/api/blacklist/1/"

    def test_list_user_suggestion_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        url: str = self.url()
        response: Response = client.get(url)
        assert response.status_code == 401

    def test_list_user_suggestion_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_user_suggestion_fails_with_normal_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_list_user_suggestion_works_with_admin_user(
        self, client: APIClient
    ) -> None:
        user: User = AdminFaker()
        url: str = self.url()
        BlackListFactory.create_batch(15)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 200
        assert response.data["count"] == 15
        assert len(response.data["results"]) == 10


@pytest.mark.django_db
class TestRetrieveBlacklistViews:
    def url(self, pk: int = None) -> str:
        if pk:
            return reverse("emails:blacklist-detail", args=[pk])
        return reverse("emails:blacklist-list")

    def test_url(self) -> None:
        assert self.url() == "/api/blacklist/"
        assert self.url(pk=1) == "/api/blacklist/1/"

    def test_retrieve_user_suggestion_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        url: str = self.url()
        response: Response = client.get(url)
        assert response.status_code == 401

    def test_retrieve_user_suggestion_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_retrieve_user_suggestion_fails_with_other_normal_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        blacklist: BlackList = BlackListFactory()
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 403

    def test_retrieve_user_suggestion_works_with_admin_user(
        self, client: APIClient
    ) -> None:
        user: User = AdminFaker()
        blacklist: BlackList = BlackListFactory()
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=user)
        response: Response = client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == blacklist.id

    def test_retrieve_user_suggestion_works_with_owner_normal_user(
        self, client: APIClient
    ) -> None:
        blacklist: BlackList = BlackListFactory()
        url: str = self.url(blacklist.id)
        client.force_authenticate(user=blacklist.user)
        response: Response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
class TestPostBlacklistViews:
    def url(self, pk: int = None) -> str:
        if pk:
            return reverse("emails:blacklist-detail", args=[pk])
        return reverse("emails:blacklist-list")

    def test_url(self) -> None:
        assert self.url() == "/api/blacklist/"
        assert self.url(pk=1) == "/api/blacklist/1/"

    def test_post_user_suggestion_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        data: dict = {"user": 2, "affairs": ""}
        url: str = self.url()
        response: Response = client.post(url, data=data)
        assert response.status_code == 401

    def test_post_user_suggestion_fails_with_user_unverified(
        self, client: APIClient
    ) -> None:
        data: dict = {"user": 2, "affairs": ""}
        user: User = UserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data)
        assert response.status_code == 403

    def test_post_user_suggestion_fails_with_other_user(
        self, client: APIClient
    ) -> None:
        other_user: User = VerifiedUserFaker()
        data: dict = {"user": other_user.id}
        user: User = VerifiedUserFaker()
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data)
        assert response.status_code == 403

    def test_post_user_suggestion_works_with_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        data: dict = {"user": user.id}
        url: str = self.url()
        client.force_authenticate(user=user)
        response: Response = client.post(url, data=data)
        # import ipdb; ipdb.set_trace()
        assert response.status_code == 201
