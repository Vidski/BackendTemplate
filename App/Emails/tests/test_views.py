import pytest

from django.core import mail

from Emails.models import Email
from Users.fakers.user import VerifiedUserFaker


ENDPOINT = '/api/v1/emails/suggestion/'


@pytest.mark.django_db
class TestSuggestionViews:
    def test_suggestion_fails_as_unauthenticate_user(self, client):
        assert len(mail.outbox) == 0
        data = {'type': 'Error', 'content': 'Error found'}
        response = client.post(ENDPOINT, data, format='json')
        assert response.status_code == 401
        assert len(mail.outbox) == 0

    def test_suggestion_creates_email_as_authenticate_user(self, client):
        normal_user = VerifiedUserFaker()
        email_count = Email.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        data = {'type': 'Error', 'content': 'Error found'}
        client.force_authenticate(user=normal_user)
        response = client.post(ENDPOINT, data, format='json')
        email_count = Email.objects.all().count()
        expected_header = f'Error from user with id: {normal_user.id}'
        assert response.status_code == 201
        assert True == response.data['was_sent']
        assert 'Error' == response.data['subject']
        assert expected_header == response.data['header']
        assert ['Error found'] == response.data['blocks']
        assert len(mail.outbox) == 0
        assert email_count == 1

    def test_suggestion_fails_as_authenticate_user_because_wrong_type(
        self, client
    ):
        normal_user = VerifiedUserFaker()
        email_count = Email.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        data = {'type': 'Wrong', 'content': 'Error found'}
        client.force_authenticate(user=normal_user)
        response = client.post(ENDPOINT, data, format='json')
        email_count = Email.objects.all().count()
        expected_error_message = 'Invalid type of suggestion'
        assert response.status_code == 400
        assert expected_error_message in response.data['detail']
        assert len(mail.outbox) == 0
        assert email_count == 0
