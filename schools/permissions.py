from rest_framework import permissions


class IsSchoolAdminOrReadOnly(permissions.BasePermission):

    def has_permissions(self, request,view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_school_admin and request.user.school is not None

    def has_object_permission(self,request,obj,view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj,'school'):
            return obj.school == request.user.school
        else:
            return obj == request.user.school
