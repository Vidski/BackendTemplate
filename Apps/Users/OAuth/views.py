from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK as OK

from Users.OAuth.serializers import FacebookOAuthSerializer
from Users.OAuth.serializers import GoogleOAuthSerializer
from Users.OAuth.serializers import TwitterOAuthSerializer


class GenericOAuthView(GenericAPIView):
    permission_classes: list = []
    serializer_class: Serializer = None

    def post(self, request: Request) -> Response:
        serializer: Serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=OK)


class GoogleOAuthView(GenericOAuthView):
    serializer_class: GoogleOAuthSerializer = GoogleOAuthSerializer


class FacebookOAuthView(GenericOAuthView):
    serializer_class: FacebookOAuthSerializer = FacebookOAuthSerializer


class TwitterOAuthView(GenericOAuthView):
    serializer_class: TwitterOAuthSerializer = TwitterOAuthSerializer
