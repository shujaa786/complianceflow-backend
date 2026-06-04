from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from documents.permissions import IsAdmin, IsApprover, IsManager, IsViewer


class DocumentPermissionTests(TestCase):
    def make_request(self, user):
        request = APIRequestFactory().get("/")
        request.user = user
        return request

    def test_is_admin_permission(self):
        user = get_user_model().objects.create_user(
            username="admin",
            password="password123",
            role="admin",
        )
        request = self.make_request(user)

        self.assertTrue(IsAdmin().has_permission(request, None))

    def test_is_manager_permission(self):
        user = get_user_model().objects.create_user(
            username="manager",
            password="password123",
            role="manager",
        )
        request = self.make_request(user)

        self.assertTrue(IsManager().has_permission(request, None))

    def test_is_approver_permission(self):
        user = get_user_model().objects.create_user(
            username="approver",
            password="password123",
            role="approver",
        )
        request = self.make_request(user)

        self.assertTrue(IsApprover().has_permission(request, None))

    def test_is_viewer_permission(self):
        user = get_user_model().objects.create_user(
            username="viewer",
            password="password123",
            role="viewer",
        )
        request = self.make_request(user)

        self.assertTrue(IsViewer().has_permission(request, None))
