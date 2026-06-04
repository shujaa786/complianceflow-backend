from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from documents.serializers import DocumentCreateSerializer


class DocumentSerializerTests(TestCase):
    def test_rejects_invalid_file_extension(self):
        payload = {
            "title": "Invalid File",
            "document_type": "invoice",
            "status": "pending",
            "description": "Bad extension.",
            "file": SimpleUploadedFile(
                "sample.txt",
                b"test content",
                content_type="text/plain",
            ),
        }

        serializer = DocumentCreateSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("file", serializer.errors)

    def test_rejects_large_file(self):
        payload = {
            "title": "Large File",
            "document_type": "invoice",
            "status": "pending",
            "description": "Too large.",
            "file": SimpleUploadedFile(
                "sample.pdf",
                b"0" * (11 * 1024 * 1024),
                content_type="application/pdf",
            ),
        }

        serializer = DocumentCreateSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("file", serializer.errors)
