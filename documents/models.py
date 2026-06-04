from django.conf import settings
from django.db import models

from .constants import (
    DOCUMENT_STATUS_CHOICES,
    DOCUMENT_TYPE_CHOICES,
    STATUS_PENDING,
)


class Document(models.Model):

    title = models.CharField(max_length=255)

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES,
    )

    status = models.CharField(
        max_length=20,
        choices=DOCUMENT_STATUS_CHOICES,
        default=STATUS_PENDING,
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