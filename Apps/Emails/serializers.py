from django.db.models import Field
from django.db.models import Model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import RelatedField
from rest_framework.serializers import ValidationError

from Emails.models.models import BlackList
from Emails.models.models import Block
from Emails.models.models import Email
from Emails.models.models import Notification
from Emails.models.models import Suggestion
from Users.models import User


class SuggestionEmailSerializer(serializers.Serializer):

    id: Field = serializers.IntegerField(read_only=True)
    user_id: Field = serializers.IntegerField()
    was_sent: Field = serializers.BooleanField(read_only=True)
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

    id: Field = serializers.IntegerField(read_only=True)
    affairs: Field = serializers.CharField(required=False)

    class Meta:
        model: Model = BlackList
        fields: str = "__all__"


class BlockSerializer(serializers.ModelSerializer):

    id: Field = serializers.IntegerField(read_only=True)
    title: Field = serializers.CharField()
    content: Field = serializers.CharField()
    show_link: Field = serializers.BooleanField(required=False)
    link_text: Field = serializers.CharField(required=False)
    link: Field = serializers.CharField(required=False)

    class Meta:
        model: Model = Block
        fields = "__all__"


class AbstractEmailSerializer(serializers.ModelSerializer):

    id: Field = serializers.IntegerField(read_only=True)
    subject: Field = serializers.CharField()
    affair: Field = serializers.CharField()
    header: Field = serializers.CharField()
    sent_date: Field = serializers.CharField(read_only=True)
    was_sent: Field = serializers.BooleanField(read_only=True)
    blocks: BlockSerializer = BlockSerializer(required=True, many=True)
    is_test: Field = serializers.BooleanField()
    programed_send_date: Field = serializers.DateTimeField()

    def update(self, instance: Model, validated_data: dict) -> Model:
        blocks_data: list = validated_data.pop("blocks")
        blocks: list = self.create_blocks(blocks_data)
        instance: Model = super().update(instance, validated_data)
        instance.blocks.set(blocks)
        return instance

    def create(self, validated_data: dict) -> Model:
        blocks_data: list = validated_data.pop("blocks")
        blocks: list = self.create_blocks(blocks_data)
        instance: Model = super().create(validated_data)
        instance.blocks.set(blocks)
        return instance

    def create_blocks(self, data: list) -> list:
        serializer: BlockSerializer = BlockSerializer(data=data, many=True)
        if not serializer.is_valid():
            raise ValidationError("Block data is not correct.")
        return serializer.create(serializer.validated_data)

    def to_representation(self, instance: Model) -> dict:
        representation: dict = super().to_representation(instance)
        blocks: list = BlockSerializer(instance.blocks.all(), many=True).data
        representation["blocks"]: list = []
        [representation["blocks"].append(dict(block)) for block in blocks]
        return representation


class NotificationSerializer(AbstractEmailSerializer):
    class Meta:
        model: Model = Notification
        fields: str = "__all__"


class EmailSerializer(AbstractEmailSerializer):

    to: Field = serializers.CharField()

    class Meta:
        model: Model = Email
        fields: str = "__all__"

    def update(self, instance: Email, validated_data: dict) -> Email:
        email: str = validated_data.pop("to")
        validated_data["to"] = get_object_or_404(User, email=email)
        return super().update(instance, validated_data)

    def create(self, validated_data: dict) -> Email:
        email: str = validated_data.pop("to")
        validated_data["to"] = get_object_or_404(User, email=email)
        return super().create(validated_data)
