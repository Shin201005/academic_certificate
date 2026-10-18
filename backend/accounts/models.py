
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ("ADMIN", "Quản trị viên"),
        ("SCHOOL", "Nhà trường"),
        ("STUDENT", "Sinh viên"),
        ("EMPLOYER", "Nhà tuyển dụng"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="STUDENT"
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="users"
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.username
