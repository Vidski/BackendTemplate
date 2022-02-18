import re as regex

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from App.utils import log_email_action
from Users.models import User

VERIFY_URL = f'{settings.URL}/api/v1/users'


def get_email_data(email_type, instance):
    data = {}
    if email_type == 'verify_email':
        data['greeting'] = f'Hi, {instance.first_name}!'
        token = instance.generate_verification_token()
        data['link'] = f'{VERIFY_URL}/{instance.id}/verify/?token={token}'
        data['content'] = settings.VERIFY_EMAIL_CONTENT
    elif email_type == 'reset_password':
        data['greeting'] = f'Hi, {instance.user.first_name}!'
        data['link'] = instance.key
        data['content'] = settings.RESET_PASSWORD_EMAIL_CONTENT
    return data


def send_email(email_type, instance):
    email_data = get_email_data(email_type, instance)
    template = render_to_string(f'{email_type}.html', email_data)
    subject = email_type.split('_')[0].capitalize()
    credential = email_type.split('_')[1]
    email = EmailMultiAlternatives(
        f'{subject} your {credential}',
        '',
        settings.EMAIL_HOST_USER,
        [
            instance.email
            if isinstance(instance, User)
            else instance.user.email
        ],
    )
    email.attach_alternative(template, 'text/html')
    email.fail_silently = False
    email.send()
    log_email_action(email_type, instance)


def get_user_or_error(requester, pk):
    """
    Get user or raise an error with a returning response
    """
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        raise NotFound('User not found')
    if not requester.is_admin and not requester.has_permission(user):
        raise PermissionDenied("You don't have permission")
    if not requester.is_verified:
        raise PermissionDenied('You have to verify your account first')
    return user


def verify_user_query_token(user, query_token):
    """
    Verify user token to verification account
    """
    token = user.generate_verification_token()
    if token != query_token:
        raise PermissionDenied("You don't have permission")


def check_e164_format(phone_number):
    """
    Checks if a phone number is in E.164 format
    example: +11234567890
    """
    regex_format = r'^\+[0-9]\d{1,20}$'
    if phone_number and not regex.match(regex_format, phone_number):
        raise ValidationError('Phone number is not valid')
