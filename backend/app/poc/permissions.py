from rest_framework import permissions
from .models import AccountUserRole


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Si l'utilisateur est un superuser Django, il est automatiquement superadmin
        if request.user.is_superuser:
            return True

        # Si l'utilisateur est un superadmin
        return request.user.is_superadmin


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Si l'utilisateur est un superadmin
        if IsSuperAdmin.has_permission(self, request, view):
            return True

        return AccountUserRole.objects.filter(
            user=request.user, account=obj.account, role="admin"
        ).exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if IsAdmin.has_object_permission(self, request, view, obj):
            return True

        # Les admins peuvent gérer les ressources de leurs comptes
        # if request.method in permissions.SAFE_METHODS:
        #    return True
        return obj.owner == request.user
