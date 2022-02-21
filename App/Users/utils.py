import re as regex

from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from Users.models import User


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
