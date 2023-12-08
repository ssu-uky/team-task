from .models import Task
from rest_framework import serializers


class CreateTaskSerializer(serializers.ModelSerializer):
    create_user = serializers.StringRelatedField(read_only=True)
    team = serializers.CharField(source="create_user.team", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Task
        fields = (
            "pk",
            "create_user",
            "team",
            "title",
            "content",
            "created_at",
        )
        read_only_fields = (
            "pk",
            "create_user",
            "team",
            "created_at",
        )


class TaskSerializer(serializers.ModelSerializer):
    create_user = serializers.StringRelatedField(read_only=True)
    team = serializers.CharField(source="create_user.team", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

        read_only_fields = (
            "pk",
            "create_user",
            "team",
            "created_at",
            "modified_at",
        )
