from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
                user.is_superuser or user.role == 'superadmin' or getattr(user, 'is_superadmin', lambda: False)()
        )


# DYNAMIC PERMISSIONS TO REGISTER USERS
class CanCreateUsers(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.method != 'POST':
            return False

        creator_role = request.user.role
        target_role = request.data.get('role')

        if creator_role == 'superadmin':
            # SuperAdmin can only create schooladmins
            return target_role == 'schooladmin'

        if creator_role == 'schooladmin':
            # SchoolAdmin can only create students or staff or depthead
            return target_role in ['student', 'staff', 'departmenthead']

        return False  # no one else may create


class CanCreateDepartmentAndClasses(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "schooladmin"


# Allows every user to access respective schools data.
class CanAccessOwnSchoolOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'school')

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'school') and obj.school == request.user.school


class IsSchoolAdminOrDeptHead(BasePermission):

    # Allows access to school admins (full) and department heads (read-only).

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role == 'schooladmin':
            return True

        if user.role == 'departmenthead' and request.method in SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'schooladmin':
            return True

        if user.role == 'departmenthead':
            # If it's a Staff object
            if hasattr(obj, 'department'):
                return obj.department == user.department

            # If it's a Student object (not allowed for depthead)
            return False

        return False
