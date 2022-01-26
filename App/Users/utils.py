from datetime import datetime
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import status

from Users.models import User

logger = logging.getLogger(__name__)

FORBIDDEN = status.HTTP_403_FORBIDDEN
NOT_FOUND = status.HTTP_404_NOT_FOUND

def get_email_data(email_type, instance):
    data = {}
    if email_type == 'verify_email':
        data['id'] = instance.id
        data['name'] = instance.first_name
        data['token'] = instance.generate_verification_token()
    elif email_type == 'reset_password':
        data['name'] = instance.user.first_name
        data['token'] = instance.key
    return data

def log_action(email_type, instance):
    if email_type == 'verify_email':
        logger.info('Users App | New us$$er, verification email sent to '\
                    f'{instance.email} at {datetime.now()}')
    else:
        logger.info('Users App | Password restore, email sent to '\
                    f'{instance.user.email} at {datetime.now()}')

def send_email(email_type, instance):
    email_data = get_email_data(email_type, instance)
    template = render_to_string(f'{email_type}.html', email_data)
    subject = email_type.split("_")[0].capitalize()
    email = EmailMultiAlternatives(f'{subject} your email',
                                    '',
                                    settings.EMAIL_HOST_USER,
                                    [instance.email if isinstance(instance, User)
                                     else instance.user.email])
    email.attach_alternative(template, "text/html")
    email.fail_silently = False
    email.send()
    log_action(email_type, instance)

def get_user_or_error(request_user, pk):
    """
    Get user or return error
    """
    try:
        instance = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response("User not found", status=NOT_FOUND)
    if not request_user.is_admin and request_user.id != instance.id:
        return Response("You don't have permission", status=FORBIDDEN)
    if not request_user.is_verified:
        return Response("You have to verify your account first", status=FORBIDDEN)
    return instance