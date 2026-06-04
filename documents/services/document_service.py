from ..models import Document


def get_document_queryset():
    return Document.objects.select_related("uploaded_by", "department").all()


def create_document(validated_data, user):
    validated_data["uploaded_by"] = user
    validated_data["department"] = user.department
    return Document.objects.create(**validated_data)
