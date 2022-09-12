from django.db.models import Field
from django.db.models import Model
from rest_framework import serializers
from rest_framework.relations import RelatedField
from rest_framework.serializers import ValidationError

from Emails.models.models import BlackList
from Emails.models.models import Block
from Emails.models.models import Notification
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


class BlockSerializer(serializers.ModelSerializer):
    """
    Block serializer
    """

    id: Field = serializers.IntegerField(read_only=True)
    title: Field = serializers.CharField()
    content: Field = serializers.CharField()
    show_link: Field = serializers.BooleanField(required=False)
    link_text: Field = serializers.CharField(required=False)
    link: Field = serializers.CharField(required=False)

    class Meta:
        model: Model = Block
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification serializer
    """

    id: Field = serializers.IntegerField(read_only=True)
    header: Field = serializers.CharField()
    affair: Field = serializers.CharField()
    subject: Field = serializers.CharField()
    is_test: Field = serializers.BooleanField()
    programed_send_date: Field = serializers.DateTimeField()
    sent_date: Field = serializers.DateTimeField(read_only=True)
    was_sent: Field = serializers.BooleanField(read_only=True)
    blocks: BlockSerializer = BlockSerializer(required=True, many=True)

    class Meta:
        model: Model = Notification
        fields = "__all__"

    def update(
        self, instance: Notification, validated_data: dict
    ) -> Notification:
        blocks_data: list = validated_data.pop("blocks")
        blocks: list = self.create_blocks(blocks_data)
        instance: Notification = super().update(instance, validated_data)
        instance.blocks.set(blocks)
        return instance

    def create(self, validated_data: dict) -> Notification:
        blocks_data: list = validated_data.pop("blocks")
        blocks: list = self.create_blocks(blocks_data)
        instance: Notification = super().create(validated_data)
        instance.blocks.set(blocks)
        return instance

    def create_blocks(self, data: list) -> list:
        serializer: BlockSerializer = BlockSerializer(data=data, many=True)
        if not serializer.is_valid():
            raise ValidationError("Block data is not correct.")
        return serializer.create(serializer.validated_data)

    def to_representation(self, instance: Notification) -> dict:
        representation: dict = super().to_representation(instance)
        blocks: list = BlockSerializer(instance.blocks.all(), many=True).data
        representation["blocks"]: list = []
        [representation["blocks"].append(dict(block)) for block in blocks]
        return representation
