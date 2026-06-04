from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import (
    DocumentCreateSerializer,
    DocumentDetailSerializer,
    DocumentListSerializer,
)
from .services.document_service import create_document, get_document_queryset


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = get_document_queryset()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "document_type", "department"]
    search_fields = ["title", "description"]
    ordering_fields = ["uploaded_at", "updated_at", "title"]
    ordering = ["-uploaded_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return DocumentListSerializer
        if self.action == "create":
            return DocumentCreateSerializer
        return DocumentDetailSerializer

    def perform_create(self, serializer):
        document = create_document(serializer.validated_data, self.request.user)
        serializer.instance = document
