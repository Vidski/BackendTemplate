from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK as OK
from rest_framework.serializers import Serializer

from SocialAuth.serializers import FacebookOAuthSerializer
from SocialAuth.serializers import GoogleOAuthSerializer
from SocialAuth.serializers import TwitterOAuthSerializer


class GenericOAuthView(GenericAPIView):
    permission_classes: list = []
    serializer_class: Serializer = None

    def post(self, request: Request) -> Response:
        serializer: Serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=OK)


class GoogleSocialAuthView(GenericOAuthView):
    serializer_class: GoogleOAuthSerializer = GoogleOAuthSerializer


class FacebookSocialAuthView(GenericOAuthView):
    serializer_class: FacebookOAuthSerializer = FacebookOAuthSerializer


class TwitterSocialAuthView(GenericOAuthView):
    serializer_class: TwitterOAuthSerializer = TwitterOAuthSerializer
