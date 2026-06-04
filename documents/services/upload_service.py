from django.core.exceptions import ValidationError
from shared.validators.file_validators import validate_document_file


def validate_upload_file(uploaded_file):
    if not uploaded_file:
        raise ValidationError("A document file is required.")

    return validate_document_file(uploaded_file)
