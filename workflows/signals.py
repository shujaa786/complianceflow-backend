from django.db.models.signals import post_save
from django.dispatch import receiver

from documents.models import Document
from accounts.models import Department
from .models import Workflow, WorkflowStep


@receiver(post_save, sender=Document)
def create_workflow_for_document(sender, instance, created, **kwargs):

    if not created:
        return

    workflow = Workflow.objects.create(
        document=instance,
        status="pending",
        current_step=1,
    )

    admin_department = Department.objects.filter(name="Administration").first()
    document_department = instance.department

    WorkflowStep.objects.bulk_create(
        [
            WorkflowStep(
                workflow=workflow,
                name=f"{document_department.name} Review",
                order=1,
                required_role="approver",
                required_department=document_department,
            ),
            WorkflowStep(
                workflow=workflow,
                name=f"{document_department.name} Manager Approval",
                order=2,
                required_role="manager",
                required_department=document_department,
            ),
            WorkflowStep(
                workflow=workflow,
                name="Final Approval",
                order=3,
                required_role="admin",
                required_department=None,
            ),
        ]
    )
