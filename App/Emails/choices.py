from django.db import models


class CommentType(models.TextChoices):
    SUGGESTION = ('S', 'SUGGESTION')
    BUG = ('B', 'BUG')
    ERROR = ('E', 'ERROR')
    OTHER = ('O', 'OTHER')
