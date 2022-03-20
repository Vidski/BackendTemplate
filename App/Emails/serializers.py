from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from Emails.models import Email


class SuggestionEmailSerializer(serializers.Serializer):
    """
    Suggestion email serializer
    """

    email_id = serializers.IntegerField(source='id')
    was_sent = serializers.BooleanField()
    subject = serializers.CharField()
    header = serializers.CharField()
    blocks = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='content'
    )

    class Meta:
        model = Email
