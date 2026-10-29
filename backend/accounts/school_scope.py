
from rest_framework.exceptions import PermissionDenied


def filter_by_school(queryset, user):
    """
    ADMIN: duoc xem tat ca du lieu.
    SCHOOL: chi duoc xem du lieu thuoc truong cua minh.
    STUDENT: khong duoc su dung ham nay de xem danh sach.
    """

    if not user.is_authenticated or not user.is_active:
        raise PermissionDenied("Ban chua duoc xac thuc.")

    if user.role == "ADMIN":
        return queryset

    if user.role == "SCHOOL" and user.school_id is not None:
        return queryset.filter(school_id=user.school_id)

    raise PermissionDenied(
        "Ban khong co quyen truy cap du lieu nay."
    )
