from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    department = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "department",
            "phone_number",
            "is_verified",
        ]