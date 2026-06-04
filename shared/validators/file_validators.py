import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from shared.constants.file_uploads import (
    ALLOWED_DOCUMENT_EXTENSIONS,
    MAX_DOCUMENT_FILE_SIZE,
)


def validate_document_file(uploaded_file):
    file_size = uploaded_file.size
    if file_size > MAX_DOCUMENT_FILE_SIZE:
        max_mb = MAX_DOCUMENT_FILE_SIZE // (1024 * 1024)
        raise ValidationError(
            _(
                "Document size must be less than %(max_mb)d MB."
            ),
            params={"max_mb": max_mb},
        )

    _, extension = os.path.splitext(uploaded_file.name or "")
    extension = extension.lower()
    if extension not in ALLOWED_DOCUMENT_EXTENSIONS:
        formatted_extensions = ", ".join(ALLOWED_DOCUMENT_EXTENSIONS)
        raise ValidationError(
            _(
                "Unsupported file format. Allowed formats: %(formats)s."
            ),
            params={"formats": formatted_extensions},
        )

    return uploaded_file
