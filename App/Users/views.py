from django.http.response import JsonResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from App.permissions import IsAdmin
from App.permissions import IsUserOwner
from App.permissions import IsVerified
from App.utils import log_information
from Users.models import User
from Users.serializers import UserLoginSerializer
from Users.serializers import UserSerializer
from Users.serializers import UserSignUpSerializer
from Users.utils import verify_user_query_token


SUCCESS = status.HTTP_200_OK
CREATED = status.HTTP_201_CREATED
UPDATED = status.HTTP_202_ACCEPTED
DELETED = status.HTTP_204_NO_CONTENT
NOT_FOUND = status.HTTP_404_NOT_FOUND


class UserViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows to interact with User model
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    normal_user_permissions = (IsAuthenticated & IsVerified & IsUserOwner)
    admin_user_permissions = (IsAuthenticated & IsAdmin)
    permission_classes = [normal_user_permissions | admin_user_permissions]

    def list(self, request):
        """
        API endpoint that allows to list all users
        """
        if not request.user.is_admin:
            raise PermissionDenied("You don't have permission")
        users = self.queryset.order_by('-created_at')
        serializer = UserSerializer(users, many=True)
        data = serializer.data
        return Response(data, status=SUCCESS)

    def retrieve(self, request, pk=None):
        """
        API endpoint that allow to get information of one user
        """
        instance = self.queryset.get(pk=pk)
        data = UserLoginSerializer(instance).data
        return Response(data, status=SUCCESS)

    def update(self, request, pk=None):
        """
        API endpoint that allow to edit an user
        """
        instance = self.queryset.get(pk=pk)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(request.data, request.user)
        user = serializer.update(instance, request.data)
        data = UserSerializer(user).data
        log_information('updated', user)
        return Response(data, status=UPDATED)

    def destroy(self, request, pk=None):
        """
        API endpoint that allow to delete an user
        """
        instance = self.queryset.get(pk=pk)
        log_information('deleted', instance)
        instance.delete()
        return Response(status=DELETED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        """
        API endpoint that allows to signup
        """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSignUpSerializer(user).data
        log_information('registered', user)
        return Response(data, status=CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        API endpoint that allows to login
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {'user': UserLoginSerializer(user).data, 'token': token}
        log_information('logged in', user)
        return JsonResponse(data, status=SUCCESS)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def verify(self, request, pk=None):
        """
        API endpoint that allows to verify user
        """
        query_token = request.query_params.get('token')
        user = self.queryset.get(pk=pk)
        verify_user_query_token(user, query_token)
        user.verify()
        data = {'user': UserLoginSerializer(user).data}
        log_information('verified', user)
        return JsonResponse(data, status=UPDATED)
