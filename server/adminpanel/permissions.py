from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Check if user is admin"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'



