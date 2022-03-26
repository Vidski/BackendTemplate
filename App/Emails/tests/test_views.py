from django.core import mail

from Emails.models import Email
from Emails.tests.abstract_test_classes import EmailsAbstractUtils


ENDPOINT = '/api/v1/emails/suggestion/'


class TestSuggestionViews(EmailsAbstractUtils):
    def test_suggestion_fails_as_unauthenticate_user(self):
        assert len(mail.outbox) == 0
        data = {'type': 'Error', 'content': 'Error found'}
        response = self.client.post(ENDPOINT, data, format='json')
        assert response.status_code == 401
        assert len(mail.outbox) == 0

    def test_suggestion_creates_email_as_authenticate_user(self):
        email_count = Email.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        data = {'type': 'Error', 'content': 'Error found'}
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(ENDPOINT, data, format='json')
        email_count = Email.objects.all().count()
        expected_header = f'Error from user with id: {self.normal_user.id}'
        assert response.status_code == 201
        assert True == response.data['was_sent']
        assert 'Error' == response.data['subject']
        assert expected_header == response.data['header']
        assert ['Error found'] == response.data['blocks']
        assert len(mail.outbox) == 0
        assert email_count == 1
