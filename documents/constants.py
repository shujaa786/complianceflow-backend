STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS_ARCHIVED = "archived"

DOCUMENT_STATUS_CHOICES = (
    (STATUS_PENDING, "Pending"),
    (STATUS_APPROVED, "Approved"),
    (STATUS_REJECTED, "Rejected"),
    (STATUS_ARCHIVED, "Archived"),
)

DOCUMENT_TYPE_INVOICE = "invoice"
DOCUMENT_TYPE_CONTRACT = "contract"
DOCUMENT_TYPE_TAX = "tax"
DOCUMENT_TYPE_EMPLOYEE = "employee"
DOCUMENT_TYPE_COMPLIANCE = "compliance"

DOCUMENT_TYPE_CHOICES = (
    (DOCUMENT_TYPE_INVOICE, "Invoice"),
    (DOCUMENT_TYPE_CONTRACT, "Contract"),
    (DOCUMENT_TYPE_TAX, "Tax Document"),
    (DOCUMENT_TYPE_EMPLOYEE, "Employee Document"),
    (DOCUMENT_TYPE_COMPLIANCE, "Compliance File"),
)
