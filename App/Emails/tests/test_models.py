from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_rest_passwordreset.models import ResetPasswordToken
import pytest
from django.core import mail
from mock import patch


from Emails.factories.block import BlockFactory
from Emails.factories.block import ResetPasswordBlockFactory
from Emails.factories.block import SuggestionBlockFactory
from Emails.factories.block import VerifyEmailBlockFactory
from Emails.factories.email import EmailFactory
from Emails.factories.email import get_subject_for_suggestion
from Emails.factories.email import ResetEmailFactory
from Emails.factories.email import SuggestionEmailFactory
from Emails.factories.email import VerifyEmailFactory
from Emails.models import Block
from Emails.models import Email
from Emails.tests.abstract_test_classes import EmailsAbstractUtils
from Users.factories.user import UserFactory


class TestEmailModel(EmailsAbstractUtils):
    def test_email_attributes(self):
        email = EmailFactory()
        dict_keys = email.__dict__.keys()
        attributes = [attribute for attribute in dict_keys]
        assert "subject" in attributes
        assert "header" in attributes
        assert "is_test" in attributes
        assert "to_all_users" in attributes
        assert "to" in attributes
        assert "programed_send_date" in attributes
        assert "sent_date" in attributes
        assert "was_sent" in attributes

    def test_email_str(self):
        email = EmailFactory()
        expected_str = f'{email.id} | {email.subject}'
        assert str(email) == expected_str

    def test_save(self):
        email = EmailFactory.build()
        email.programed_send_date = None
        email.to = "email@test.com, email2@test.com"
        email.is_test = False
        assert email.programed_send_date is None
        assert email.to == "email@test.com, email2@test.com"
        assert email.is_test is False
        email.save()
        assert email.programed_send_date is not None
        assert email.to == "email@test.com, email2@test.com"

    def test_saving_an_email_without_date(self):
        email = EmailFactory.build()
        email.programed_send_date = None
        email.to = "email@test.com, email2@test.com"
        email.is_test = False
        assert email.programed_send_date is None
        assert email.is_test is False
        email.save()
        assert email.programed_send_date is not None

    def test_saving_an_email_with_emails(self):
        email = EmailFactory.build()
        email.to = "email@test.com, email2@test.com"
        email.is_test = False
        assert email.to == "email@test.com, email2@test.com"
        assert email.is_test is False
        email.save()
        assert email.to == "email@test.com, email2@test.com"

    def test_saving_an_email_with_emails_as_test(self):
        email = EmailFactory.build()
        email.to = "email@test.com, email2@test.com"
        email.is_test = True
        assert email.to == "email@test.com, email2@test.com"
        assert email.is_test is True
        email.save()
        assert email.to == f"{settings.TEST_EMAIL}"

    def test_saving_an_email_with_emails_to_all_users(self):
        email = EmailFactory.build()
        email.to = "email@test.com, email2@test.com"
        email.is_test = False
        email.to_all_users = True
        assert email.to == "email@test.com, email2@test.com"
        assert email.is_test is False
        assert email.to_all_users is True
        email.save()
        assert email.to == f"{self.admin_user}, {self.normal_user}"

    def test_get_emails_with_emails(self):
        email = EmailFactory(
            to = "email@test.com, email2@test.com"
        )
        assert email.to == "email@test.com, email2@test.com"

    def test_get_emails_with_emails_as_test(self):
        email = EmailFactory(
            to = "email@test.com, email2@test.com",
            is_test = True
        )
        assert email.to == f"{settings.TEST_EMAIL}"

    def test_get_emails_with_emails_to_all_users(self):
        email = EmailFactory(
            to = "email@test.com, email2@test.com",
            is_test = False,
            to_all_users = True
        )
        assert email.to == f"{self.admin_user}, {self.normal_user}"

    def test_get_emails_data_with_blocks(self):
        block = BlockFactory()
        email = EmailFactory(blocks=[
            block
        ])
        data = email.get_email_data()
        assert data["header"] == email.header
        assert list(data["blocks"]) == list(email.blocks.all())

    def test_get_emails_data_without_blocks(self):
        email = EmailFactory(blocks=None)
        email.blocks.all().delete()
        data = email.get_email_data()
        assert data["header"] == email.header
        assert data["blocks"] == []

    def test_get_template(self):
        email = EmailFactory()
        data = email.get_email_data()
        template = email.get_template()
        expected_template = render_to_string('email.html', data)
        assert template == expected_template

    def test_get_email_object(self):
        email = EmailFactory()
        email_object = email.get_email_object()
        assert isinstance(email_object, EmailMultiAlternatives)

    def test_send_email(self):
        assert len(mail.outbox) == 0
        email = EmailFactory()
        email.send()
        assert email.was_sent is True
        assert len(mail.outbox) == 1


class TestBlockModel(EmailsAbstractUtils):
    def test_block_attributes(self):
        block = BlockFactory()
        dict_keys = block.__dict__.keys()
        attributes = [attribute for attribute in dict_keys]
        assert "title" in attributes
        assert "content" in attributes
        assert "show_link" in attributes
        assert "link_text" in attributes
        assert "link" in attributes

    def test_block_str(self):
        block = BlockFactory()
        expected_str = f'{block.id} | {block.title}'
        assert str(block) == expected_str
