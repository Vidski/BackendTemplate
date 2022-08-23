from django.http import HttpRequest
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from Emails.models.models import BlackList
from Users.models import User


class IsBlacklistOwner(BasePermission):
    message: str = "You don't have permission to modify this blacklist item"

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        user: User = request.user
        kwargs: dict = request.parser_context["kwargs"]
        blacklist_id: int = kwargs.get("pk", None)
        blacklist: BlackList = get_object_or_404(BlackList, id=blacklist_id)
        return user.has_permission(blacklist)


class HasBlacklistPetitionPermission(IsBlacklistOwner):
    message: str = "You don't have permission to perform this action"

    def is_a_get_type_request(self, request: HttpRequest, _type: str) -> bool:
        is_get_method: bool = request.method == "GET"
        has_empty_kwargs: bool = request.parser_context["kwargs"] == {}
        if _type and _type == "retrieve":
            return is_get_method and has_empty_kwargs
        if _type and _type == "list":
            return is_get_method and not has_empty_kwargs

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if self.is_a_get_type_request(request, _type="list"):
            return False
        if self.is_a_get_type_request(request, _type="retrieve"):
            return True
        if request.method == "POST":
            id_in_body: int = int(request.data["user"])
            return id_in_body == request.user.id
        return super().has_permission(request, view)
