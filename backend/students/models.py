
from django.db import models
from django.conf import settings
from schools.models import School


class Student(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="students"
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile"
    )

    student_code = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    email = models.EmailField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["school", "student_code"],
                name="unique_student_per_school"
            )
        ]

    def __str__(self):
        return f"{self.student_code} - {self.full_name}"
