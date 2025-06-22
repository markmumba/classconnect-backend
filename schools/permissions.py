from rest_framework import permissions


class IsSchoolAdminOrReadOnly(permissions.BasePermissions):

    def has_permissions(self, request):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_school_admin

    def has_object_permission(self,request,obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj,'school'):
            return obj.school == request.user.school
        else:
            return obj == request.user.school
