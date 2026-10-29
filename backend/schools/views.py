from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin, IsAdminOrSchool
from .models import School
from .serializers import SchoolSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrSchool,
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return School.objects.all().order_by("id")

        if user.role == "SCHOOL" and user.school_id is not None:
            return School.objects.filter(
                id=user.school_id
            )

        return School.objects.none()

    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                IsAuthenticated(),
                IsAdmin(),
            ]

        return super().get_permissions()