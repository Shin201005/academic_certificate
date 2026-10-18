
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    school_code = models.CharField(
        max_length=50,
        unique=True
    )
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
