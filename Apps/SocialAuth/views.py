from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK as OK

from SocialAuth.serializers import GoogleOAuthSerializer


class GoogleSocialAuthView(GenericAPIView):
    permission_classes: list = []

    def post(self, request) -> Response:
        data: dict = request.data
        serializer: GoogleOAuthSerializer = GoogleOAuthSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=OK)
