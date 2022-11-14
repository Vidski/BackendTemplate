from django.contrib.auth import password_validation
from django.db.models import Field
from django.db.models import Model
from django.db.models import QuerySet
from drf_extra_fields.fields import Base64ImageField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.relations import RelatedField
from rest_framework.serializers import BooleanField
from rest_framework.serializers import CharField
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import EmailField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.serializers import Serializer
from rest_framework.serializers import ValidationError

from Users.models import Profile
from Users.models import User
from Users.utils import check_e164_format


class UserRetrieveSerializer(Serializer):
    """
    User authentication serializer
    """

    id: Field = IntegerField(read_only=True)
    first_name: Field = CharField(required=False, max_length=255)
    last_name: Field = CharField(required=False, max_length=255)
    email: Field = EmailField(required=True)
    phone_number: PhoneNumberField = PhoneNumberField(
        required=False, max_length=22
    )
    is_verified: Field = BooleanField(read_only=True)
    is_premium: Field = BooleanField(read_only=True)
    is_admin: Field = BooleanField(read_only=True)
    created_at: Field = DateTimeField(read_only=True)
    updated_at: Field = DateTimeField(read_only=True)

    class Meta:
        model: Model = User


class UserUpdateSerializer(ModelSerializer):
    """
    User custom serializer
    """

    first_name: Field = CharField(required=False, max_length=255)
    last_name: Field = CharField(required=False, max_length=255)
    email: Field = EmailField(required=False)
    phone_number: CharField = CharField(
        required=False,
        max_length=22,
        allow_blank=True,
        allow_null=True,
    )
    old_password: Field = CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True
    )
    password: Field = CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True
    )

    def update(self, instance: User, validated_data: dict) -> User:
        password: str = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def validate_email(self, email: str) -> None:
        user: User = self.context["request"].user
        user_with_email: User = User.objects.filter(email=email).first()
        if user_with_email and not user.has_permission(user_with_email):
            raise ValidationError("Email is taken")
        return email

    def validate_phone_number(self, phone_number: str) -> None:
        if not phone_number:
            return None
        check_e164_format(phone_number)
        queryset: QuerySet = User.objects.filter(phone_number=phone_number)
        user_with_phone: User = queryset.first()
        user: User = self.context["request"].user
        if user_with_phone and not user.has_permission(user_with_phone):
            raise ValidationError("Phone number is taken")
        return phone_number

    def validate_password(self, password: str) -> None:
        if not password:
            return None
        old_password: str = self.initial_data.get("old_password", None)
        if not old_password:
            raise ValidationError("Old password is required")
        user: User = self.context["request"].user
        if not user.is_admin and not user.check_password(old_password):
            raise ValidationError("Wrong password")
        password_validation.validate_password(password)
        return password

    class Meta:
        model: Model = User
        fields: list = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "old_password",
            "password",
        ]


class ProfileSerializer(ModelSerializer):
    """
    Profile serializer
    """

    bio: CharField = CharField(
        required=False, allow_blank=True, allow_null=True
    )
    nickname: CharField = CharField(
        required=False, allow_blank=True, allow_null=True
    )
    image: Base64ImageField = Base64ImageField(required=False, allow_null=True)
    user_id: RelatedField = PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", required=False
    )

    class Meta:
        model: Model = Profile
        fields: list = [
            "id",
            "user_id",
            "nickname",
            "bio",
            "image",
        ]

    def is_valid(self, raise_exception: bool = False) -> dict:
        is_valid: dict = super().is_valid(raise_exception)
        self.check_user_field_according_requester(self.validated_data)
        return is_valid

    def validate_nickname(self, nickname: str) -> None:
        if nickname:
            profile: QuerySet = Profile.objects.filter(nickname=nickname)
            if profile.exists() and self.instance != profile.first():
                raise ValidationError("This nickname already exists.")
        return nickname

    def check_user_field_according_requester(
        self, validated_data: dict
    ) -> None:
        requester: str = self.context["request"].user
        if not requester.is_admin:
            self.validated_data["user"] = self.instance.user
        else:
            self.check_profile_with_user(validated_data)

    def check_profile_with_user(self, validated_data: dict) -> None:
        user: User or None = validated_data.get("user", None)
        user_id: int = getattr(user, "id", None)
        profile: QuerySet = Profile.objects.filter(user_id=user_id)
        if profile.exists() and self.instance != profile.first():
            raise ValidationError("User profile already exists")
