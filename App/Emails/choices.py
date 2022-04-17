from django.db import models


class CommentType(models.TextChoices):
    SUGGESTION = ('S', 'Suggestion')
    BUG = ('B', 'Bug')
    ERROR = ('E', 'Error')
    OTHER = ('O', 'Other')
