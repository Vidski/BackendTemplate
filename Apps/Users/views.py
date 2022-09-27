from django.db.models import QuerySet
from django.http import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Project.pagination import ListTenResultsSetPagination
from Project.utils.log import log_information
from Users.models import Profile
from Users.models import User
from Users.permissions import IsActionAllowed
from Users.permissions import IsAdmin
from Users.permissions import IsProfileOwner
from Users.permissions import IsUserOwner
from Users.permissions import IsVerified
from Users.serializers import ProfileSerializer, UserRetrieveSerializer
from Users.serializers import UserLoginSerializer
from Users.serializers import UserUpdateSerializer
from Users.serializers import UserSignUpSerializer
from Users.utils import verify_user_query_token


SUCCESS: int = status.HTTP_200_OK
CREATED: int = status.HTTP_201_CREATED
DELETED: int = status.HTTP_204_NO_CONTENT
NOT_FOUND: int = status.HTTP_404_NOT_FOUND


class UserViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows to interact with User model
    """

    queryset: QuerySet = User.objects.all().order_by("-created_at")
    serializer_class: UserUpdateSerializer = UserUpdateSerializer
    user_permissions: bool = IsAuthenticated & IsVerified & IsUserOwner
    admin_user_permissions: bool = IsAuthenticated & IsAdmin
    permission_classes: list = [user_permissions | admin_user_permissions]
    pagination_class: PageNumberPagination = ListTenResultsSetPagination

    def list(self, request: HttpRequest) -> Response:
        """
        API endpoint that allows to list all users
        """
        page: list = self.paginate_queryset(self.queryset)
        serializer: UserRetrieveSerializer = UserRetrieveSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request: HttpRequest, pk: int = None) -> Response:
        """
        API endpoint that allow to get information of one user
        """
        instance: User = self.queryset.get(pk=pk)
        data: UserRetrieveSerializer = UserRetrieveSerializer(instance).data
        return Response(data, status=SUCCESS)

    def update(self, request: HttpRequest, pk: int = None) -> Response:
        """
        API endpoint that allow to edit an user
        """
        instance: User = self.queryset.get(pk=pk)
        serializer: UserUpdateSerializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(request.data, request.user)
        user: User = serializer.update(instance, request.data)
        data: dict = UserUpdateSerializer(user).data
        log_information("updated", user)
        return Response(data, status=SUCCESS)

    def destroy(self, request: HttpRequest, pk: int = None) -> Response:
        """
        API endpoint that allow to delete an user
        """
        instance: User = self.queryset.get(pk=pk)
        log_information("deleted", instance)
        instance.delete()
        return Response(status=DELETED)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request: HttpRequest) -> Response:
        """
        API endpoint that allows to signup
        """
        serializer: UserSignUpSerializer = UserSignUpSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        log_information("registered", user)
        return Response(serializer.data, status=CREATED)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request: HttpRequest) -> JsonResponse:
        """
        API endpoint that allows to login
        """
        serializer: UserLoginSerializer = UserLoginSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        log_information("logged in", serializer.user)
        return JsonResponse(serializer.data, status=SUCCESS)

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def verify(self, request: HttpRequest, pk: int = None) -> JsonResponse:
        """
        API endpoint that allows to verify user
        """
        query_token: str = request.query_params.get("token")
        user: User = self.queryset.get(pk=pk)
        verify_user_query_token(user, query_token)
        user.verify()
        data: dict = {"user": UserLoginSerializer(user).data}
        log_information("verified", user)
        return JsonResponse(data, status=SUCCESS)


class ProfileViewSet(viewsets.ModelViewSet):
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
