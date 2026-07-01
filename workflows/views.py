from drf_spectacular.utils import extend_schema
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Workflow,
    WorkflowStep,
    ApprovalAction,
    ApprovalActionType,
    WorkflowStatus,
    WorkflowComment,
)
from .serializers import WorkflowSerializer, WorkflowCommentSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        workflow = self.get_object()

        if workflow.status in [
            WorkflowStatus.APPROVED,
            WorkflowStatus.REJECTED,
        ]:
            return Response(
                {"error": "Workflow already completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_step = workflow.steps.filter(order=workflow.current_step).first()

        if not current_step:
            return Response(
                {"error": "No active workflow step found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if current_step.is_completed:
            return Response(
                {"error": "This step has already been completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------
        # Dynamic Role Validation
        # -----------------------------
        required_role = current_step.required_role

        if request.user.role != required_role:
            return Response(
                {
                    "error": (
                        f"Only users with role "
                        f"'{required_role}' can approve this step."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # -----------------------------
        # Dynamic Department Validation
        # -----------------------------
        required_department = current_step.required_department

        if required_department and request.user.department != required_department:
            return Response(
                {
                    "error": (
                        f"This step belongs to "
                        f"{required_department.name} department."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        ApprovalAction.objects.create(
            workflow=workflow,
            step=current_step,
            reviewer=request.user,
            action=ApprovalActionType.APPROVED,
            comments=request.data.get("comments"),
        )

        current_step.is_completed = True
        current_step.completed_by = request.user
        current_step.completed_at = timezone.now()
        current_step.save()

        next_step = workflow.steps.filter(order=workflow.current_step + 1).first()

        if next_step:
            workflow.current_step += 1
            workflow.status = WorkflowStatus.IN_PROGRESS
        else:
            workflow.status = WorkflowStatus.APPROVED
            workflow.document.status = "approved"
            workflow.document.save()

        workflow.save()

        return Response(
            {
                "message": "Step approved successfully.",
                "current_step": workflow.current_step,
                "workflow_status": workflow.status,
            }
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        workflow = self.get_object()

        if workflow.status in [
            WorkflowStatus.APPROVED,
            WorkflowStatus.REJECTED,
        ]:
            return Response(
                {"error": "Workflow already completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_step = workflow.steps.filter(order=workflow.current_step).first()

        if not current_step:
            return Response(
                {"error": "No active workflow step found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------
        # Dynamic Role Validation
        # -----------------------------
        required_role = current_step.required_role

        if request.user.role != required_role:
            return Response(
                {
                    "error": (
                        f"Only users with role "
                        f"'{required_role}' can reject this step."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # -----------------------------
        # Dynamic Department Validation
        # -----------------------------
        required_department = current_step.required_department

        if required_department and request.user.department != required_department:
            return Response(
                {
                    "error": (
                        f"This step belongs to "
                        f"{required_department.name} department."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        ApprovalAction.objects.create(
            workflow=workflow,
            step=current_step,
            reviewer=request.user,
            action=ApprovalActionType.REJECTED,
            comments=request.data.get("comments"),
        )

        current_step.completed_by = request.user
        current_step.completed_at = timezone.now()
        current_step.save()

        workflow.status = WorkflowStatus.REJECTED
        workflow.document.status = "rejected"

        workflow.document.save()
        workflow.save()

        return Response(
            {
                "message": "Workflow rejected successfully.",
                "workflow_status": workflow.status,
            }
        )

    @action(detail=True, methods=["get"])
    def timeline(self, request, pk=None):
        workflow = self.get_object()

        actions = (
            ApprovalAction.objects.filter(workflow=workflow)
            .select_related("reviewer", "step")
            .order_by("created_at")
        )

        data = []

        for action in actions:
            data.append(
                {
                    "step": action.step.name,
                    "reviewer": action.reviewer.username,
                    "action": action.action,
                    "comments": action.comments,
                    "created_at": action.created_at,
                }
            )

        return Response(data)

    @extend_schema(
        responses=WorkflowCommentSerializer(many=True),
    )
    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        workflow = self.get_object()

        comments = workflow.comments.select_related("user").order_by("created_at")

        serializer = WorkflowCommentSerializer(
            comments,
            many=True,
        )

        return Response(serializer.data)

    @extend_schema(
        request=WorkflowCommentSerializer,
        responses=WorkflowCommentSerializer,
    )
    @comments.mapping.post
    def add_comment(self, request, pk=None):
        workflow = self.get_object()

        serializer = WorkflowCommentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        WorkflowComment.objects.create(
            workflow=workflow,
            user=request.user,
            comment=serializer.validated_data["comment"],
        )

        return Response(
            {"message": "Comment added successfully."},
            WorkflowCommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )
