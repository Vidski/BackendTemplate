from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Emails.views import BlacklistViewSet
from Emails.views import EmailViewSet
from Emails.views import NotificationViewSet
from Emails.views import SuggestionViewSet


router: DefaultRouter = DefaultRouter()
router.register("emails", EmailViewSet, basename="emails")
router.register("suggestions", SuggestionViewSet, basename="suggestions")
router.register("blacklist", BlacklistViewSet, basename="blacklist")
router.register("notifications", NotificationViewSet, basename="notifications")

urlpatterns: list = [
    path("", include(router.urls)),
]
