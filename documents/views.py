from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer


class DocumentListCreateView(generics.ListCreateAPIView):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Document.objects.all().order_by("-uploaded_at")

        status_param = self.request.query_params.get("status")
        doc_type = self.request.query_params.get("document_type")

        if status_param:
            queryset = queryset.filter(status=status_param)

        if doc_type:
            queryset = queryset.filter(document_type=doc_type)

        return queryset

    def perform_create(self, serializer):

        serializer.save(
            uploaded_by=self.request.user,
            department=self.request.user.department
        )


class DocumentDetailView(generics.RetrieveAPIView):

    queryset = Document.objects.all()

    serializer_class = DocumentSerializer

    permission_classes = [IsAuthenticated]