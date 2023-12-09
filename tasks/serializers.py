from rest_framework import serializers
from .models import Task, SubTask, Team

from users.models import User


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


class TinyTaskSerializer(serializers.ModelSerializer):
    task_pk = serializers.SerializerMethodField()
    # create_user = serializers.StringRelatedField(read_only=True)
    team = serializers.CharField(source="create_user.team", read_only=True)
    sub_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "task_pk",
            "team",
            # "create_user",
            "title",
            "is_complete",
            "sub_tasks",
        )

    def get_task_pk(self, obj):
        return obj.pk

    def get_sub_tasks(self, obj):
        sub_tasks = obj.subtasks.filter(is_complete=False)
        serializer = TinySubTaskSerializer(sub_tasks, many=True)
        return serializer.data


class TaskSerializer(serializers.ModelSerializer):
    task_pk = serializers.SerializerMethodField()
    create_user = serializers.StringRelatedField(read_only=True)
    team = serializers.CharField(source="create_user.team", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Task
        fields = (
            "task_pk",
            "team",
            "create_user",
            "title",
            "content",
            "is_complete",
            "completed_date",
            "created_at",
            "modified_at",
        )

        read_only_fields = (
            "task_pk",
            "create_user",
            "team",
            "created_at",
            "modified_at",
        )

    def get_task_pk(self, obj):
        return obj.pk


class SubTaskSerializer(serializers.ModelSerializer):
    # task_pk = serializers.SerializerMethodField()
    subtask_pk = serializers.SerializerMethodField()
    team = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Team.objects.all(),
        required=False,
    )

    class Meta:
        model = SubTask
        fields = (
            "subtask_pk",
            "team",
            "sub_title",
            "sub_content",
            "is_complete",
            "completed_date",
        )

    def get_subtask_pk(self, obj):
        return obj.pk


class NewSubTaskSerializer(serializers.ModelSerializer):
    # task_pk = serializers.SerializerMethodField()
    subtask_pk = serializers.SerializerMethodField()
    team = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Team.objects.all(),
        required=False,
    )

    class Meta:
        model = SubTask
        fields = (
            # "task_pk",
            "subtask_pk",
            "team",
            "sub_title",
            "sub_content",
            "is_complete",
            "completed_date",
        )
    
    # def get_task_pk(self, obj):
    #     return obj.task.pk

    def get_subtask_pk(self, obj):
        return obj.pk
    
    # def create(self, validated_data):
    #     task = validated_data.get("task")
    #     team = validated_data.get("team")
    #     sub_title = validated_data.get("sub_title")
    #     sub_content = validated_data.get("sub_content")

    #     subtask = SubTask.objects.create(
    #         task=task,
    #         sub_title=sub_title,
    #         sub_content=sub_content,
    #     )
    #     subtask.team.add(*team)

    #     return subtask


class TinySubTaskSerializer(serializers.ModelSerializer):
    subtask_pk = serializers.SerializerMethodField()
    team = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Team.objects.all(),
        required=False,
    )

    class Meta:
        model = SubTask
        fields = (
            "subtask_pk",
            "team",
            "sub_title",
            "is_complete",
        )

    def get_subtask_pk(self, obj):
        return obj.pk
