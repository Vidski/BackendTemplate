import pytest
from django.core import mail
from rest_framework.test import APIClient

from Emails.factories.email import SuggestionEmailFactory
from Emails.models import Suggestion
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker


@pytest.fixture(scope='function')
def client():
    return APIClient()


BASE_ENDPOINT = '/api/suggestions'


@pytest.mark.django_db
class TestSuggestionViews:

    ACTION = 'submit'
    ENDPOINT = f'{BASE_ENDPOINT}/{ACTION}/'

    def test_suggestion_fails_as_unauthenticate_user(self, client):
        assert len(mail.outbox) == 0
        data = {'type': 'Error', 'content': 'Error found'}
        response = client.post(self.ENDPOINT, data, format='json')
        assert response.status_code == 401
        assert len(mail.outbox) == 0

    def test_suggestion_creates_email_as_authenticate_user(self, client):
        normal_user = VerifiedUserFaker()
        email_count = Suggestion.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        data = {'type': 'ERROR', 'content': 'Error found'}
        client.force_authenticate(user=normal_user)
        response = client.post(self.ENDPOINT, data, format='json')
        email_count = Suggestion.objects.all().count()
        expected_header = f'ERROR from user with id: {normal_user.id}'
        assert response.status_code == 201
        assert True == response.data['was_sent']
        assert 'ERROR' == response.data['subject']
        assert expected_header == response.data['header']
        block = Suggestion.objects.first().blocks.first()
        assert [block.id] == response.data['blocks']
        assert 'Error found' == response.data['content']
        assert len(mail.outbox) == 0
        assert email_count == 1

    def test_suggestion_fails_as_authenticate_user_because_wrong_type(
        self, client
    ):
        normal_user = VerifiedUserFaker()
        email_count = Suggestion.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        data = {'type': 'Wrong', 'content': 'Error found'}
        client.force_authenticate(user=normal_user)
        response = client.post(self.ENDPOINT, data, format='json')
        email_count = Suggestion.objects.all().count()
        expected_error_message = 'Invalid type of suggestion'
        assert response.status_code == 400
        assert expected_error_message in response.data['detail']
        assert len(mail.outbox) == 0
        assert email_count == 0


@pytest.mark.django_db
class TestReadSuggestionViews:

    ACTION = 'read'

    def test_read_suggestion_fails_as_unauthenticate_user(self, client):
        user = UserFaker()
        type = 'ERROR'
        content = 'Error found'
        suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        pk = suggestion.pk
        url = f'{BASE_ENDPOINT}/{pk}/{self.ACTION}/'
        response = client.post(url, format='json')
        assert response.status_code == 401

    def test_suggestion_creates_email_as_authenticate_user(self, client):
        normal_user = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        user = UserFaker()
        type = 'ERROR'
        content = 'Error found'
        suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        assert suggestion.was_read == False
        pk = suggestion.pk
        url = f'{BASE_ENDPOINT}/{pk}/{self.ACTION}/'
        response = client.post(url, format='json')
        assert response.status_code == 200
        suggestion.refresh_from_db()
        assert suggestion.was_read == True
