from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Emails.views import EmailViewSet


router = DefaultRouter()
router.register('emails', EmailViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
