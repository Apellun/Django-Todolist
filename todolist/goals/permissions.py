from rest_framework.permissions import BasePermission, SAFE_METHODS


class EntityEditPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.method not in SAFE_METHODS:
            if obj.user != request.user:
                return False
        
        return True