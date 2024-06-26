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
    team = serializers.CharField(source="create_user.team", read_only=True)
    sub_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "task_pk",
            "team",
            "title",
            "is_complete",
            "sub_tasks",
        )

    def get_task_pk(self, obj):
        return obj.pk

    def get_sub_tasks(self, obj):
        sub_tasks = obj.subtasks.all()
        serializer = TinySubTaskSerializer(sub_tasks, many=True)
        return serializer.data


class TaskSerializer(serializers.ModelSerializer):
    task_pk = serializers.SerializerMethodField()
    create_user = serializers.StringRelatedField(read_only=True)
    team = serializers.CharField(source="create_user.team", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    completed_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    total_subtasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "task_pk",
            "total_subtasks",
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

    def get_total_subtasks(self, obj):
        return obj.subtasks.count()


class TaskListSerializer(serializers.ModelSerializer):
    task_pk = serializers.SerializerMethodField()
    team = serializers.CharField(source="create_user.team", read_only=True)
    total_subtasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "task_pk",
            "team",
            "title",
            "is_complete",
            "total_subtasks",
        )

    def get_task_pk(self, obj):
        return obj.pk

    def get_total_subtasks(self, obj):
        return obj.subtasks.count()


class SubTaskSerializer(serializers.ModelSerializer):
    # task_pk = serializers.SerializerMethodField()
    task_team = serializers.CharField(source="task.create_user.team", read_only=True)
    subtask_pk = serializers.SerializerMethodField()
    # subtask_create_user = serializers.StringRelatedField(read_only=True)
    team = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Team.objects.all(),
        required=False,
    )
    completed_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = SubTask
        fields = (
            # "task_pk",
            "task_team",
            "subtask_pk",
            "team",
            "sub_title",
            "sub_content",
            "is_complete",
            "completed_date",
            # "subtask_create_user",
        )
    
    # def get_task_pk(self, obj):
    #     return obj.task.pk

    def get_subtask_pk(self, obj):
        return obj.pk


class SubTaskListSerializer(serializers.ModelSerializer):
    task_pk = serializers.SerializerMethodField()
    subtask_pk = serializers.SerializerMethodField()
    task_team = serializers.CharField(source="task.create_user.team", read_only=True)
    team = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Team.objects.all(),
        required=False,
    )

    class Meta:
        model = SubTask
        fields = (
            "task_team",
            "task_pk",
            "subtask_pk",
            "team",
            "sub_title",
            "is_complete",
        )

    def get_task_pk(self, obj):
        return obj.task.pk

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
