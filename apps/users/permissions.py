from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.users.models import CRMUser


class IsCRMUser(BasePermission):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return hasattr(request.user, 'crm_user')


class IsManager(IsCRMUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            crm_user = request.user.crm_user
            return crm_user and crm_user.role == CRMUser.MANAGER
        return False


class IsManagerOrReadOnly(IsCRMUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            crm_user = request.user.crm_user
            return crm_user and (crm_user.role == CRMUser.MANAGER) or request.method in SAFE_METHODS
        return False


class IsAdmin(IsCRMUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            crm_user = request.user.crm_user
            return crm_user and crm_user.role == CRMUser.ADMIN
        return False


class IsAdminOrReadOnly(IsCRMUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            crm_user = request.user.crm_user
            return crm_user and (crm_user.role == CRMUser.ADMIN) or request.method in SAFE_METHODS
        return False


class AllowReadAny(BasePermission):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.method in SAFE_METHODS
        return False
