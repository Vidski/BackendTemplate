from django.db.models import TextChoices


class CommentType(TextChoices):
    SUGGESTION: str = "SUGGESTION"
    BUG: str = "BUG"
    ERROR: str = "ERROR"
    OTHER: str = "OTHER"


class EmailAffair(TextChoices):
    NOTIFICATION: str = "NOTIFICATION"
    PROMOTION: str = "PROMOTION"
    GENERAL: str = "GENERAL"
    SETTINGS: str = "SETTINGS"
    INVOICE: str = "INVOICE"
    SUGGESTION: str = "SUGGESTION"
