from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from Users.models import User


class IsAdmin(BasePermission):
    message = "You don't have permission"

    def has_permission(self, request, view):
        return request.user.is_admin


class IsVerified(BasePermission):
    message = 'You have to verify your account first'

    def has_permission(self, request, view):
        return request.user.is_verified


class IsUserOwner(BasePermission):
    message = "You don't have permission"

    def has_permission(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            user = get_object_or_404(User, id=pk)
        except:
            return False
        return request.user.has_permission(user)
