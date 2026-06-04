from rest_framework import serializers

from .models import Document
from .services.upload_service import validate_upload_file


class DocumentListSerializer(serializers.ModelSerializer):
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
            "uploaded_at",
            "updated_at",
        ]
        read_only_fields = (
            "uploaded_by",
            "uploaded_at",
            "updated_at",
        )


class DocumentDetailSerializer(DocumentListSerializer):

    class Meta(DocumentListSerializer.Meta):
        fields = DocumentListSerializer.Meta.fields + ["description"]


class DocumentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = [
            "title",
            "document_type",
            "status",
            "file",
            "description",
        ]

    def validate_file(self, value):
        return validate_upload_file(value)
