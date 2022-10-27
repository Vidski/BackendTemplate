from django.http import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from Project.utils.log import log_information
from Users.Auth.serializers import UserLoginSerializer
from Users.Auth.serializers import UserSignUpSerializer
from Users.models import User
from Users.serializers import UserRetrieveSerializer


SUCCESS: int = status.HTTP_200_OK
CREATED: int = status.HTTP_201_CREATED


class UserAuthViewSet(ViewSet):
    """
    API endpoint that allows to authenticate users
    """

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request: HttpRequest) -> Response:
        data: dict = request.data
        language: str = data.pop("preferred_language", None)
        serializer: UserSignUpSerializer = UserSignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        user.create_profile(language)
        return Response(UserRetrieveSerializer(user).data, status=CREATED)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request: HttpRequest) -> JsonResponse:
        serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        log_information("logged in", serializer.user)
        return JsonResponse(serializer.data, status=SUCCESS)
