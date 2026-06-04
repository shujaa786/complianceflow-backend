from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Department
from documents.models import Document


class DocumentModelTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Legal")
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password123",
        )
        self.document = Document.objects.create(
            title="Policy Review",
            document_type="invoice",
            status="pending",
            file="documents/test.pdf",
            uploaded_by=self.user,
            department=self.department,
        )

    def test_document_str_returns_title(self):
        self.assertEqual(str(self.document), "Policy Review")
