from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Users.Auth.views import UserAuthViewSet


router: DefaultRouter = DefaultRouter()
router.register("auth", UserAuthViewSet, basename="auth")

urlpatterns: list = [
    path("", include(router.urls)),
]
