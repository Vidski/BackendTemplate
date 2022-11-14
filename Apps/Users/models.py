from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models import CASCADE
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import EmailField
from django.db.models import Field
from django.db.models import ImageField
from django.db.models import Model
from django.db.models import OneToOneField
from django.db.models import TextField
from django.db.models.fields.related import ForeignObject
from django_prometheus.models import ExportModelOperationsMixin
from phonenumber_field.modelfields import PhoneNumberField

from Project.storage import ImageStorage
from Project.storage import get_image_storage
from Project.storage import image_file_upload
from Users.choices import AuthProviders
from Users.choices import GenderChoices
from Users.choices import PreferredLanguageChoices
from Users.manager import CustomUserManager


class User(
    ExportModelOperationsMixin("user"), AbstractBaseUser, PermissionsMixin
):
    username: None = None
    is_superuser: None = None
    last_login: None = None

    email: Field = EmailField(
        "Email address",
        unique=True,
        error_messages={"unique": "This email already exists."},
    )
    first_name: Field = CharField("First name", null=False, max_length=50)
    last_name: Field = CharField("Last name", null=False, max_length=50)
    phone_number: PhoneNumberField = PhoneNumberField(
        "Phone number",
        null=True,
        blank=True,
        max_length=22,
        unique=True,
        error_messages={"unique": "This number already exists."},
    )
    gender: Field = CharField(
        "Gender",
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.NOT_SAID,
        null=True,
    )
    birth_date: Field = DateField("Birth date", null=True, auto_now_add=False)
    preferred_language: Field = CharField(
        "Preferred language",
        max_length=2,
        choices=PreferredLanguageChoices.choices,
        default=PreferredLanguageChoices.ENGLISH,
        null=True,
    )
    is_verified: Field = BooleanField("Verified", default=False)
    is_premium: Field = BooleanField("Premium", default=False)
    is_admin: Field = BooleanField("Admin", default=False)
    auth_provider: Field = CharField(
        "Auth provider",
        max_length=10,
        choices=AuthProviders.choices,
        default=AuthProviders.EMAIL,
        null=True,
    )
    created_at: Field = DateTimeField("Creation date", auto_now_add=True)
    updated_at: Field = DateTimeField("Update date", auto_now=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list = ["first_name", "last_name"]

    objects: BaseUserManager = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def create_profile(self) -> None:
        if not Profile.objects.filter(user=self).exists():
            Profile.objects.create(user=self)

    def has_perm(self, permission: str, object: Model = None) -> bool:
        return self.is_admin

    def has_permission(self, object: Model = None) -> bool:
        if isinstance(object, User):
            return object.id == self.id
        else:
            return object.user.id == self.id

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_admin

    def verify(self) -> None:
        self.is_verified = True
        if not Profile.objects.filter(user=self).exists():
            Profile.objects.create(user=self)
        self.save()

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self) -> bool:
        return self.is_admin

    @property
    def is_adult(self) -> bool:
        if not self.birth_date:
            return None
        adultness: datetime = datetime.now() - relativedelta(years=18)
        birthday: datetime = datetime.strptime(str(self.birth_date), "%Y-%m-%d")
        return birthday < adultness


class Profile(ExportModelOperationsMixin("profile"), Model):
    user: ForeignObject = OneToOneField(
        User,
        on_delete=CASCADE,
        related_name="profile",
    )
    nickname: Field = CharField(
        "Nick",
        unique=True,
        error_messages={"unique": "This nickname already exists."},
        null=True,
        blank=True,
        max_length=50,
    )
    bio: Field = TextField("Bio", null=True, blank=True)
    image: Field = ImageField(
        "Profile image",
        storage=get_image_storage(),
        upload_to=image_file_upload,
        null=True,
        blank=True,
    )
    created_at: Field = DateTimeField("Creation date", auto_now_add=True)
    updated_at: Field = DateTimeField("Update date", auto_now=True)

    def __str__(self) -> str:
        return f"User ({self.user_id}) profile ({self.pk})"
