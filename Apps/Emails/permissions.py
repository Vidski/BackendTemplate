from django.http import HttpRequest
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.permissions import DjangoObjectPermissions

from Emails.models.models import BlackList
from Users.models import User


class IsBlacklistOwner(BasePermission):
    message: str = "You don't have permission to modify this blacklist item"

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        user: User = request.user
        blacklist_id: int = request.parser_context["kwargs"]["pk"]
        blacklist: BlackList = get_object_or_404(BlackList, id=blacklist_id)
        return user.has_permission(blacklist)
