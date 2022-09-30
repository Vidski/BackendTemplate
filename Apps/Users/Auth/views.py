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
    API endpoint that allows to interact with User model
    """

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
        user_data: dict = UserRetrieveSerializer(user).data
        return Response(user_data, status=CREATED)

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
