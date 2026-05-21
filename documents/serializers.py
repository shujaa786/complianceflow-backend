from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    uploaded_by = serializers.StringRelatedField()
    department = serializers.StringRelatedField()

    class Meta:
        model = Document

        fields = [
            "id",
            "title",
            "document_type",
            "status",
            "file",
            "uploaded_by",
            "department",
            "description",
            "uploaded_at",
            "updated_at",
        ]

        read_only_fields = (
            "uploaded_by",
            "uploaded_at",
            "updated_at",
        )