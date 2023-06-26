from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticated().has_permission(request, view) and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (IsAuthenticated().has_permission(request, view)
                    and request.user.is_admin))
