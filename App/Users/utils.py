import re as regex

from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError


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
