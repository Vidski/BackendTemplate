from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Emails.factories.email import SuggestionEmailFactory as SuggestionEmail
from Emails.serializers import SuggestionEmailSerializer
from Users.models import User


CREATED = status.HTTP_201_CREATED


class EmailViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to create a suggestion email
    """

    @action(
        detail=False, methods=['post'], permission_classes=[IsAuthenticated]
    )
    def suggestion(self, request):
        type = request.data.get('type')
        if type not in settings.SUGGESTION_TYPES:
            raise ParseError('Invalid type of suggestion')
        content = request.data.get('content')
        user = User.objects.get(id=request.user.id)
        email = SuggestionEmail(type=type, content=content, instance=user)
        email.send()
        data = SuggestionEmailSerializer(email).data
        return Response(data=data, status=CREATED)
