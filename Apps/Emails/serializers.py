from django.db.models import Field
from django.db.models import Model
from rest_framework import serializers
from rest_framework.relations import RelatedField

from Emails.models.models import BlackList
from Emails.models.models import Suggestion


class SuggestionEmailSerializer(serializers.Serializer):
    """
    Suggestion serializer
    """

    id: Field = serializers.IntegerField()
    user_id: Field = serializers.IntegerField()
    was_sent: Field = serializers.BooleanField()
    was_read: Field = serializers.BooleanField()
    subject: Field = serializers.CharField()
    header: Field = serializers.CharField()
    blocks: RelatedField = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="id"
    )
    content: Field = serializers.CharField(source="blocks.first.content")

    class Meta:
        model: Model = Suggestion


class BlacklistSerializer(serializers.ModelSerializer):
    """
    Blacklist serializer
    """

    id: Field = serializers.IntegerField(read_only=True)
    affairs: Field = serializers.CharField(required=False)

    class Meta:
        model: Model = BlackList
        fields: str = "__all__"
