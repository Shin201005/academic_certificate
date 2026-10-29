
from rest_framework.permissions import BasePermission


ALLOWED_ROLES = ("ADMIN", "SCHOOL", "STUDENT")


class IsAllowedRole(BasePermission):
    message = "Tai khoan khong co vai tro hop le."

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_active
            and user.role in ALLOWED_ROLES
        )


class IsAdmin(BasePermission):
    message = "Chi ADMIN duoc phep truy cap."

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_active
            and user.role == "ADMIN"
        )


class IsSchool(BasePermission):
    message = "Chi SCHOOL duoc phep truy cap."

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_active
            and user.role == "SCHOOL"
            and user.school_id is not None
        )


class IsStudent(BasePermission):
    message = "Chi STUDENT duoc phep truy cap."

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_active
            and user.role == "STUDENT"
        )


class IsAdminOrSchool(BasePermission):
    message = "Chi ADMIN hoac SCHOOL duoc phep truy cap."

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated or not user.is_active:
            return False

        if user.role == "ADMIN":
            return True

        return (
            user.role == "SCHOOL"
            and user.school_id is not None
        )


class IsSameSchoolOrAdmin(BasePermission):
    message = "Ban khong co quyen truy cap du lieu truong khac."

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_active
            and (
                user.role == "ADMIN"
                or (
                    user.role == "SCHOOL"
                    and user.school_id is not None
                )
            )
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "ADMIN":
            return True

        school_id = getattr(obj, "school_id", None)

        return (
            user.role == "SCHOOL"
            and user.school_id is not None
            and school_id == user.school_id
        )
