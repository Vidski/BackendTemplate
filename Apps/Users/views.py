from django.db.models import Model
from django.db.models import QuerySet
from django.dispatch import receiver
from django.http import HttpRequest
from django.http.response import JsonResponse
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK as SUCCESS
from rest_framework.views import View
from rest_framework.viewsets import ModelViewSet

from Emails.utils import send_email
from Project.pagination import ListTenResultsSetPagination
from Project.utils.log import log_information
from Users.models import Profile
from Users.models import User
from Users.permissions import IsActionAllowed
from Users.permissions import IsAdmin
from Users.permissions import IsProfileOwner
from Users.permissions import IsUserOwner
from Users.permissions import IsVerified
from Users.serializers import ProfileSerializer
from Users.serializers import UserRetrieveSerializer
from Users.serializers import UserUpdateSerializer
from Users.utils import verify_user_query_token


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows to interact with User model
    """

    queryset: QuerySet = User.objects.all().order_by("-created_at")
    user_permissions: bool = IsAuthenticated & IsVerified & IsUserOwner
    admin_user_permissions: bool = IsAuthenticated & IsAdmin
    permission_classes: list = [user_permissions | admin_user_permissions]
    pagination_class: PageNumberPagination = ListTenResultsSetPagination

    def get_serializer_class(self) -> Serializer:
        if self.action == "update":
            return UserUpdateSerializer
        return UserRetrieveSerializer

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def verify(self, request: HttpRequest, pk: int = None) -> JsonResponse:
        """
        API endpoint that allows to verify user
        """
        query_token: str = request.query_params.get("token")
        user: User = self.queryset.get(pk=pk)
        verify_user_query_token(user, query_token)
        user.verify()
        log_information("verified", user)
        data: dict = {"user": user.id, "verified": True}
        return JsonResponse(data, status=SUCCESS)


class ProfileViewSet(ModelViewSet):
    """
    API endpoint that allows to interact with Profile model;
    List, create and destroy are only available only for admin users because the
    create and destroy will be triggered when verify/delete the user instance
    """

    queryset: QuerySet = Profile.objects.all().order_by("-created_at")
    lookup_url_kwarg: str = "pk"
    serializer_class: ProfileSerializer = ProfileSerializer
    user_permissions: bool = IsVerified & IsProfileOwner & IsActionAllowed
    admin_user_permissions: bool = IsAdmin
    permissions: bool = user_permissions | admin_user_permissions
    permission_classes: list = [IsAuthenticated & permissions]
    pagination_class: PageNumberPagination = ListTenResultsSetPagination


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender: View,
    instance: Model,
    reset_password_token: Model,
    *args: tuple,
    **kwargs: dict,
) -> None:
    send_email("reset_password", reset_password_token)
