from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from SocialAuth.views import FacebookSocialAuthView
from SocialAuth.views import GoogleSocialAuthView
from SocialAuth.views import TwitterSocialAuthView


urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view()),
    path("facebook/", FacebookSocialAuthView.as_view()),
    path("twitter/", FacebookSocialAuthView.as_view()),
]

# router: DefaultRouter = DefaultRouter()
# router.register("google", GoogleSocialAuthView, basename="google")

# urlpatterns: list = [
#     path("google", include(router.urls)),
# ]
