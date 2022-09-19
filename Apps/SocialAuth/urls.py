from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from SocialAuth.views import GoogleSocialAuthView


urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view()),
]

# router: DefaultRouter = DefaultRouter()
# router.register("google", GoogleSocialAuthView, basename="google")

# urlpatterns: list = [
#     path("google", include(router.urls)),
# ]
