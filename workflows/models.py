from django.db import models
from django.conf import settings
from documents.models import Document


class WorkflowStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class ApprovalActionType(models.TextChoices):
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    REQUEST_CHANGES = "request_changes", "Request Changes"


class Workflow(models.Model):
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, related_name="workflow"
    )

    status = models.CharField(
        max_length=20, choices=WorkflowStatus.choices, default=WorkflowStatus.PENDING
    )

    current_step = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.document.title} - {self.status}"


class WorkflowStep(models.Model):
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, related_name="steps"
    )

    name = models.CharField(max_length=255)

    order = models.PositiveIntegerField()

    required_role = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Role allowed to complete this workflow step.",
    )

    required_department = models.ForeignKey(
        "accounts.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Department allowed to complete this step.",
    )

    assigned_role = models.CharField(max_length=50)

    is_completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class ApprovalAction(models.Model):
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, related_name="actions"
    )

    step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE)

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    action = models.CharField(max_length=50, choices=ApprovalActionType.choices)

    comments = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer} - {self.action}"


class WorkflowComment(models.Model):
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="workflow_comments",
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} " f"commented on Workflow #{self.workflow.id}"
