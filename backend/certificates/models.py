
from django.db import models
from schools.models import School
from students.models import Student


class Certificate(models.Model):
    STATUS_CHOICES = [
        ("DRAFT", "Bản nháp"),
        ("ISSUED", "Đã cấp"),
        ("REVOKED", "Đã thu hồi"),
    ]

    certificate_code = models.CharField(
        max_length=100,
        unique=True
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="certificates"
    )

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="certificates"
    )

    title = models.CharField(max_length=255)
    major = models.CharField(
        max_length=255,
        blank=True
    )
    issue_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.certificate_code


class CertificateFile(models.Model):
    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
        related_name="files"
    )

    file = models.FileField(
        upload_to="certificates/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )


class BlockchainRecord(models.Model):
    certificate = models.OneToOneField(
        Certificate,
        on_delete=models.PROTECT,
        related_name="blockchain_record"
    )

    data_hash = models.CharField(max_length=64)

    transaction_hash = models.CharField(
        max_length=66,
        unique=True
    )

    block_number = models.BigIntegerField(
        null=True,
        blank=True
    )

    recorded_at = models.DateTimeField(
        auto_now_add=True
    )
