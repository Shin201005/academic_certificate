
import uuid
from django.db import models
from django.conf import settings
from certificates.models import Certificate


class VerificationLog(models.Model):
    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verification_logs"
    )

    verification_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_valid = models.BooleanField(default=False)

    checked_at = models.DateTimeField(
        auto_now_add=True
    )
