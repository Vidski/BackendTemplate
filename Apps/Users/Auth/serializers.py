from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.db.models import Field
from django.db.models import Model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import BooleanField
from rest_framework.serializers import CharField
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import EmailField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import Serializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken

from Emails.utils import send_email
from Project.utils.log import log_information
from Users.choices import PreferredLanguageChoices
from Users.models import User
from Users.serializers import ProfileSerializer


class UserAuthSerializer(Serializer):
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
    profile: ProfileSerializer = ProfileSerializer(read_only=True)
    token: Field = SerializerMethodField(read_only=True)
    refresh_token: Field = SerializerMethodField(read_only=True)

    def get_token(self, object: User) -> str:
        return str(AccessToken.for_user(object))

    def get_refresh_token(self, object: User) -> str:
        return str(RefreshToken.for_user(object).access_token)

    class Meta:
        model: Model = User


class UserLoginSerializer(Serializer):
    """
    User login serializer
    """

    email: Field = EmailField(required=True)
    password: Field = CharField(write_only=True, required=True)

    def is_valid(self, raise_exception: bool = True) -> bool:
        super().is_valid(raise_exception=raise_exception)
        self.validate_login(self.initial_data)
        self._data = UserAuthSerializer(self.user).data
        return True

    def validate_login(self, data: dict) -> None:
        user: User = authenticate(
            email=data["email"], password=data["password"]
        )
        if not user:
            raise ValidationError("Invalid credentials")
        if not user.is_verified:
            raise ValidationError("User is not verified")
        self.user: User = user

    class Meta:
        model: Model = User


class UserSignUpSerializer(Serializer):
    """
    User sign up serializer
    """

    first_name: Field = CharField(required=True, max_length=255)
    last_name: Field = CharField(required=True, max_length=255)
    email: Field = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password: Field = CharField(
        write_only=True, min_length=8, max_length=64, required=True
    )
    password_confirmation: Field = CharField(
        write_only=True, min_length=8, max_length=64, required=True
    )
    preferred_language: Field = CharField(
        write_only=True, min_length=2, max_length=2, required=False
    )

    def validate_password(self, password: str) -> str:
        password_confirmation = self.initial_data["password_confirmation"]
        if password != password_confirmation:
            raise ValidationError("Password confirmation does not match")
        password_validation.validate_password(password)
        return password

    def validate_preferred_language(self, preferred_language: str) -> str:
        if preferred_language not in PreferredLanguageChoices.values:
            return PreferredLanguageChoices.ENGLISH
        return preferred_language

    def create(self, data):
        data.pop("password_confirmation")
        user: User = User.objects.create_user(**data, is_verified=False)
        send_email("verify_email", user)
        log_information("registered", user)
        return user
