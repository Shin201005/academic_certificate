from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accounts.permissions import IsAdminOrSchool
from accounts.school_scope import filter_by_school

from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):

    serializer_class = StudentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrSchool,
    ]

    def get_queryset(self):
        return filter_by_school(
            Student.objects.all().order_by("id"),
            self.request.user
        )

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == "SCHOOL":
            serializer.save(school_id=user.school_id)
        else:
            serializer.save()

    def perform_update(self, serializer):
        user = self.request.user

        if user.role == "SCHOOL":
            if serializer.instance.school_id != user.school_id:
                raise PermissionDenied(
                    "Khong duoc sua sinh vien truong khac."
                )

            serializer.save(school_id=user.school_id)
        else:
            serializer.save()