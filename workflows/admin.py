from django.contrib import admin

from .models import (
    Workflow,
    WorkflowStep,
    ApprovalAction,
    WorkflowComment,
)

admin.site.register(Workflow)
admin.site.register(WorkflowStep)
admin.site.register(ApprovalAction)
admin.site.register(WorkflowComment)
