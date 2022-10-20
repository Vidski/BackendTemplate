from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK as OK
from rest_framework.status import HTTP_201_CREATED as CREATED
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.models import BlackList
from Emails.models import Email
from Emails.models import Notification
from Emails.models import Suggestion
from Emails.permissions import HasBlacklistPetitionPermission
from Emails.serializers import BlacklistSerializer
from Emails.serializers import EmailSerializer
from Emails.serializers import NotificationSerializer
from Emails.serializers import SuggestionEmailSerializer
from Project.pagination import ListTenResultsSetPagination
from Users.models import User
from Users.permissions import IsAdmin
from Users.permissions import IsSameUserId
from Users.permissions import IsVerified


class EmailViewSet(ModelViewSet):
    queryset: QuerySet = Email.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: EmailSerializer = EmailSerializer
    pagination_class: PageNumberPagination = ListTenResultsSetPagination
    permission_classes: list = [IsAuthenticated & IsVerified & IsAdmin]


class BlacklistViewSet(ModelViewSet):
    queryset: QuerySet = BlackList.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: BlacklistSerializer = BlacklistSerializer
    pagination_class: PageNumberPagination = ListTenResultsSetPagination
    permission_classes: list = [
        IsAuthenticated
        & IsVerified
        & (IsAdmin | HasBlacklistPetitionPermission)
    ]


class NotificationViewSet(ModelViewSet):
    queryset: QuerySet = Notification.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: NotificationSerializer = NotificationSerializer
    pagination_class: PageNumberPagination = ListTenResultsSetPagination
    permission_classes: list = [IsAuthenticated & IsVerified & IsAdmin]


class SuggestionViewSet(GenericViewSet):
    SUBMIT_PERMISSIONS: list = [IsAuthenticated & IsVerified]
    LIST_PERMISSIONS: list = [IsAuthenticated & (IsAdmin | IsSameUserId)]
    READ_PERMISSIONS: list = [IsAuthenticated & IsAdmin]
    queryset: QuerySet = Suggestion.objects.all().order_by("-id")
    pagination_class: PageNumberPagination = ListTenResultsSetPagination

    @action(
        detail=False, methods=["post"], permission_classes=SUBMIT_PERMISSIONS
    )
    def submit(self, request: HttpRequest) -> Response:
        type: str = request.data.get("type")
        content: str = request.data.get("content")
        user: User = User.objects.get(id=request.user.id)
        suggestion: Suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        suggestion.send()
        data = SuggestionEmailSerializer(suggestion).data
        return Response(data=data, status=CREATED)

    @action(detail=True, methods=["post"], permission_classes=READ_PERMISSIONS)
    def read(self, request: HttpRequest, pk: int = None) -> Response:
        suggestion: Suggestion = get_object_or_404(Suggestion, pk=pk)
        suggestion.was_read = True
        suggestion.save()
        data: dict = SuggestionEmailSerializer(suggestion).data
        return Response(data=data, status=OK)

    @action(detail=False, methods=["get"], permission_classes=LIST_PERMISSIONS)
    def user(self, request: HttpRequest) -> Response:
        user_id: int = request.GET.get("user_id", request.user.id)
        suggestions: QuerySet = self.queryset.filter(user_id=user_id)
        page: QuerySet = self.paginate_queryset(suggestions)
        data: dict = SuggestionEmailSerializer(page, many=True).data
        return self.get_paginated_response(data)
