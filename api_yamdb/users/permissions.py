from rest_framework import permissions

NOT_SAFE_METHODS = ('DELETE',)


class AdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin():
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_admin():
            return True
        return request.user.is_superuser


class AdminUserMore(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin():
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
           or request.user.is_admin()):
            return True

        return request.user.is_superuser
