from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Emails.choices import CommentType
from Emails.factories.suggestion import \
    SuggestionEmailFactory as SuggestionEmail
from Emails.models import Suggestion
from Emails.serializers import SuggestionEmailSerializer
from Users.models import User


CREATED = status.HTTP_201_CREATED


class SuggestionViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to create a suggestion email
    """

    PERMISSIONS = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=PERMISSIONS)
    def submit(self, request):
        type = request.data.get('type')
        if type.upper() not in CommentType.names:
            raise ParseError('Invalid type of suggestion')
        content = request.data.get('content')
        user = User.objects.get(id=request.user.id)
        suggestion = SuggestionEmail(type=type, content=content, user=user)
        suggestion.send()
        data = SuggestionEmailSerializer(suggestion).data
        return Response(data=data, status=CREATED)

    @action(detail=True, methods=['post'], permission_classes=PERMISSIONS)
    def read(self, request, pk=None):
        suggestion = get_object_or_404(Suggestion, pk=pk)
        suggestion.was_read = True
        suggestion.save()
        data = SuggestionEmailSerializer(suggestion).data
        return Response(data=data, status=status.HTTP_200_OK)
