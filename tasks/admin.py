from django.contrib import admin
from .models import Task, SubTask, Team


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "content",
        "is_complete",
        "completed_date",
        "created_at",
        "modified_at",
    )
    list_display_links = (
        "pk",
        "title",
    )
    list_filter = ("is_complete",)
    search_fields = (
        "title",
        "content",
    )


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "task",
        "subtask_create_user",
        "sub_title",
        "sub_content",
        "is_complete",
        "completed_date",
        "created_at",
        "modified_at",
    )
    list_display_links = ("pk", "task")
    list_filter = ("is_complete",)
    search_fields = ("sub_title", "sub_content")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    list_display_links = (
        "pk",
        "name",
    )
    search_fields = ("name",)
