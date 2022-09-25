from django.urls import path

from SocialAuth.views import FacebookSocialAuthView
from SocialAuth.views import GoogleSocialAuthView
from SocialAuth.views import TwitterSocialAuthView


urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view(), name="google"),
    path("facebook/", FacebookSocialAuthView.as_view(), name="facebook"),
    path("twitter/", TwitterSocialAuthView.as_view(), name="twitter"),
]
