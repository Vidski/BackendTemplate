from django.urls import path

from OAuth.views import FacebookOAuthView
from OAuth.views import GoogleOAuthView
from OAuth.views import TwitterOAuthView


urlpatterns = [
    path("google/", GoogleOAuthView.as_view(), name="google"),
    path("facebook/", FacebookOAuthView.as_view(), name="facebook"),
    path("twitter/", TwitterOAuthView.as_view(), name="twitter"),
]
