from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "document_type",
        "status",
        "uploaded_by",
        "department",
        "uploaded_at",
    )

    list_filter = (
        "status",
        "document_type",
        "department",
    )

    search_fields = (
        "title",
    )