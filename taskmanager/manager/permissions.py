from rest_framework import permissions


class GroupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user in obj.assigned_users.all()


class TaskPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_superuser or request.user in obj.group.assigned_users.all()
        return request.user.is_superuser or request.user in (obj.creating_user, obj.assigned_user)
