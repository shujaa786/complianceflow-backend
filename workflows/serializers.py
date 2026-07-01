from rest_framework import serializers

from .models import (
    Workflow,
    WorkflowStep,
    ApprovalAction,
    WorkflowComment,
)


class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = "__all__"


class ApprovalActionSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source="reviewer.username", read_only=True)

    class Meta:
        model = ApprovalAction
        fields = "__all__"


class WorkflowSerializer(serializers.ModelSerializer):

    steps = WorkflowStepSerializer(many=True, read_only=True)

    actions = ApprovalActionSerializer(many=True, read_only=True)

    document_title = serializers.CharField(source="document.title", read_only=True)

    class Meta:
        model = Workflow
        fields = "__all__"


class WorkflowCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = WorkflowComment
        fields = [
            "id",
            "username",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = (
            "id",
            "username",
            "created_at",
            "updated_at",
        )
