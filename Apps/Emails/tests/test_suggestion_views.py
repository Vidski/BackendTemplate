from django.core import mail
from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Emails.choices import CommentType
from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.models import Suggestion
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import User


@fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@mark.django_db
class TestSubmitSuggestionViews:
    def url(self) -> str:
        return f"{reverse('emails:suggestions-submit')}"

    def test_url(self) -> None:
        assert self.url() == "/api/suggestions/submit/"

    def test_suggestion_fails_as_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        assert len(mail.outbox) == 0
        data: dict = {"type": "Error", "content": "Error found"}
        response: Response = client.post(self.url(), data, format="json")
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
        response: Response = client.post(self.url(), data, format="json")
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
        response: Response = client.post(self.url(), data, format="json")
        email_count: Suggestion = Suggestion.objects.all().count()
        expected_error_message: str = "Type not allowed"
        assert response.status_code == 400
        assert expected_error_message in response.data["detail"]
        assert len(mail.outbox) == 0
        assert email_count == 0


@mark.django_db
class TestReadSuggestionViews:
    def url(self, suggestion_id: int) -> str:
        return f"{reverse('emails:suggestions-read', args=[suggestion_id])}"

    def test_url(self) -> None:
        assert self.url(1) == "/api/suggestions/1/read/"

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
        response: Response = client.post(self.url(pk), format="json")
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
        response: Response = client.post(self.url(pk), format="json")
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
        response: Response = client.post(self.url(pk), format="json")
        assert response.status_code == 200
        suggestion.refresh_from_db()
        assert suggestion.was_read == True


@mark.django_db
class TestUserSuggestionViews:

    ACTION: str = "user"

    def url(self, user_id: int = None) -> str:
        if user_id is None:
            return f"{reverse('emails:suggestions-user')}"
        return f"{reverse('emails:suggestions-user')}?user_id={user_id}"

    def test_url(self) -> None:
        assert self.url(1) == "/api/suggestions/user/?user_id=1"
        assert self.url() == "/api/suggestions/user/"

    def test_list_user_suggestion_without_user_id_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        response: Response = client.get(self.url())
        assert response.status_code == 401

    def test_list_user_suggestion_with_user_id_fails_as_unauthenticated(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        response: Response = client.get(self.url(user.id))
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
        response: Response = client.get(self.url(other_user.id))
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
        response: Response = client.get(self.url(user.id))
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
        response: Response = client.get(self.url())
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
        response: Response = client.get(self.url(user.id))
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["count"] == Suggestion.objects.count()
