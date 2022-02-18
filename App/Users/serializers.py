from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField

from Users.models import User
from Users.utils import check_e164_format
from Users.utils import send_email


class UserSerializer(serializers.ModelSerializer):
    """
    User custom serializer
    """

    def is_valid(self, data, user):
        """
        Main validation method overwritted to check user data when update method
        is called. This is because the creation of an user as well is validated on signup
        method and the main validation method is executed before "validate" one
        """
        email = data.get('email', None)
        self.check_email(email, user)
        phone_number = data.get('phone_number', None)
        self.check_phone_number(phone_number, user)
        self.check_password(data, user)
        return data

    def create(self, validated_data):
        """
        Create a new user
        """
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, data):
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('last_name', instance.last_name)
        instance.email = data.get('email', instance.email)
        instance.phone_number = data.get('phone_number', instance.phone_number)
        password = data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def check_email(self, email, user):
        user_with_email = User.objects.filter(email=email).first()
        if user_with_email and not user.has_permission(user_with_email):
            raise ValidationError('Email is taken')

    def check_phone_number(self, phone_number, user):
        check_e164_format(phone_number)
        user_with_phone_number = User.objects.filter(
            phone_number=phone_number
        ).first()
        if user_with_phone_number and not user.has_permission(
            user_with_phone_number
        ):
            raise ValidationError('Phone number is taken')

    def check_password(self, data, user):
        password = data.get('password', None)
        if password:
            old_password = data.get('old_password', None)
            if not old_password:
                raise ValidationError(
                    'Old password is required to set a new one'
                )
            old_password_is_valid = user.check_password(old_password) == True
            if not old_password_is_valid:
                raise ValidationError('Wrong password')
            password_validation.validate_password(password)

    class Meta:
        model = User
        fields = [
            'first_name',
            'phone_number',
            'email',
            'created_at',
            'updated_at',
        ]


class UserAuthSerializer(serializers.Serializer):
    """
    User authentication serializer
    """

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=False, max_length=255)
    last_name = serializers.CharField(required=False, max_length=255)
    phone_number = PhoneNumberField(required=False, max_length=22)
    is_verified = serializers.BooleanField(read_only=True)
    is_premium = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, min_length=8, max_length=64, required=True
    )


class UserLoginSerializer(UserAuthSerializer):
    """
    User login serializer
    """

    def validate(self, data):
        """
        Validate user login data
        """
        email, password = self.check_email_and_password(data)
        user = authenticate(email=email, password=password)
        if not user:
            raise ValidationError('Invalid credentials')
        if not user.is_verified:
            raise ValidationError('User is not verified')
        self.context['user'] = user
        return data

    def check_email_and_password(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise ValidationError('Email and password are required')
        return email, password

    def create(self, data):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token
        return user, str(token)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'created_at',
            'updated_at',
        ]


class UserSignUpSerializer(UserAuthSerializer):
    """
    User sign up serializer
    """

    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password_confirmation = serializers.CharField(
        write_only=True, min_length=8, max_length=64, required=False
    )

    def validate(self, data):
        """
        Validate to create a new user
        """
        password = data.get('password')
        password_confirmation = data.get('password_confirmation', None)
        if not password_confirmation:
            raise ValidationError('Password confirmation is required')
        if password != password_confirmation:
            raise ValidationError('Password confirmation does not match')
        password_validation.validate_password(password)
        return data

    def create(self, data):
        """
        Create a new user
        """
        data.pop('password_confirmation')
        if 'phone_number' in data:
            data.pop('phone_number')
        user = User.objects.create_user(**data, is_verified=False)
        send_email('verify_email', user)
        return user
