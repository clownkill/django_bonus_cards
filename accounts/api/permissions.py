from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and request.user.is_superuser
        elif view.action == 'create':
            return True
        elif view.action == 'retrieve' and request.user.is_staff:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action == 'retrieve':
            print(obj.id, request.user.id)
            return obj.id == request.user.id or request.user.is_superuser
        elif view.action in ['update', 'partial_update']:
            return obj.id == request.user.id or request.user.is_superuser
        elif view.action == 'destroy':
            return request.user.is_superuser
        else:
            return False