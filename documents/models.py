from django.db import models
from django.conf import settings


class Document(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("archived", "Archived"),
    )

    DOCUMENT_TYPES = (
        ("invoice", "Invoice"),
        ("contract", "Contract"),
        ("tax", "Tax Document"),
        ("employee", "Employee Document"),
        ("compliance", "Compliance File"),
    )

    title = models.CharField(max_length=255)

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    file = models.FileField(
        upload_to="documents/"
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_documents"
    )

    department = models.ForeignKey(
        "accounts.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title