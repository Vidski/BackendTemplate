from django.db.models import Field
from django.db.models import Model
from rest_framework.generics import get_object_or_404
from rest_framework.relations import RelatedField
from rest_framework.serializers import BooleanField
from rest_framework.serializers import CharField
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework.serializers import SlugRelatedField

from Emails.models import BlackList
from Emails.models import Block
from Emails.models import Email
from Emails.models import Notification
from Emails.models import Suggestion
from Users.models import User


class SuggestionEmailSerializer(Serializer):

    id: Field = IntegerField(read_only=True)
    user_id: Field = IntegerField()
    was_sent: Field = BooleanField(read_only=True)
    was_read: Field = BooleanField()
    subject: Field = CharField()
    header: Field = CharField()
    blocks: RelatedField = SlugRelatedField(
        many=True, read_only=True, slug_field="id"
    )
    content: Field = CharField(source="blocks.first.content")

    class Meta:
        model: Model = Suggestion


class BlacklistSerializer(ModelSerializer):

    id: Field = IntegerField(read_only=True)
    affairs: Field = CharField(required=False)

    class Meta:
        model: Model = BlackList
        fields: str = "__all__"


class BlockSerializer(ModelSerializer):

    id: Field = IntegerField(read_only=True)
    title: Field = CharField()
    content: Field = CharField()
    show_link: Field = BooleanField(required=False)
    link_text: Field = CharField(required=False)
    link: Field = CharField(required=False)

    class Meta:
        model: Model = Block
        fields = "__all__"


class AbstractEmailSerializer(ModelSerializer):

    id: Field = IntegerField(read_only=True)
    subject: Field = CharField()
    affair: Field = CharField()
    header: Field = CharField()
    sent_date: Field = CharField(read_only=True)
    was_sent: Field = BooleanField(read_only=True)
    blocks: BlockSerializer = BlockSerializer(required=True, many=True)
    is_test: Field = BooleanField()
    programed_send_date: Field = DateTimeField()

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
        serializer.is_valid(raise_exception=True)
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

    to: Field = CharField()

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
