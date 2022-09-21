from django.db.models import TextChoices


class GenderChoices(TextChoices):
    FEMALE: tuple = ("F", "Female")
    MALE: tuple = ("M", "Male")
    NON_BINARY: tuple = ("N", "Non-binary")
    NOT_SAID: tuple = ("P", "Prefer not to say")


class PreferredLanguageChoices(TextChoices):
    ENGLISH: tuple = ("EN", "English")
    SPANISH: tuple = ("ES", "Spanish")
    FRENCH: tuple = ("FR", "French")
    OTHER: tuple = ("OT", "Other")


class AuthProviders(TextChoices):
    EMAIL: tuple = ("email", "Email")
    FACEBOOK: tuple = ("facebook", "Facebook")
    GOOGLE: tuple = ("google", "Google")
    Twitter: tuple = ("twitter", "Twitter")
    Apple: tuple = ("apple", "Apple")
