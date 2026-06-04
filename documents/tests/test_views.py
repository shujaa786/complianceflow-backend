from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Department
from documents.models import Document


class DocumentViewSetTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password123",
        )
        self.department = Department.objects.create(name="Legal")
        self.user.department = self.department
        self.user.save()
        self.client.force_authenticate(user=self.user)

        for index in range(12):
            Document.objects.create(
                title=f"Document {index}",
                document_type="invoice",
                status="pending" if index % 2 == 0 else "approved",
                file="documents/sample.pdf",
                uploaded_by=self.user,
                department=self.department,
                description=f"Document {index} description.",
            )

    def test_list_documents_returns_paginated_results(self):
        url = reverse("document-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 10)

    def test_filters_by_status_and_searches_title(self):
        url = reverse("document-list")
        response = self.client.get(url, {"status": "approved", "search": "Document 1"})

        self.assertEqual(response.status_code, 200)
        results = response.data["results"]
        self.assertTrue(all(item["status"] == "approved" for item in results))
        self.assertTrue(any("Document 1" in item["title"] for item in results))

    def test_orders_documents_by_title(self):
        url = reverse("document-list")
        response = self.client.get(url, {"ordering": "title"})

        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.data["results"]]
        self.assertEqual(titles, sorted(titles))
