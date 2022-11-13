from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Model


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields: dict,
    ) -> Model:
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email: str = self.normalize_email(email)
        user: Model = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields: dict,
    ) -> Model:
        """
        Create and save a SuperUser with the given email and password.
        """
        user: Model = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_verified = True
        user.is_premium = True
        user.save(using=self._db)
        return user
