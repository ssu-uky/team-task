from django.db import models

from users.models import User


class Team(models.Model):
    name = models.CharField(
        max_length=50,
        choices=User.TeamChoices.choices,
        unique=True,
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    create_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="create_user",
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
    )
    team = models.ManyToManyField(
        Team,
        related_name="subtasks_teams",
        blank=True,
    )
    subtask_create_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subtask_create_user",
    )
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    sub_content = models.TextField(blank=True, null=True)

    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        team_names = ", ".join([team.name for team in self.team.all()])
        return f"{self.task.title} - Teams: {team_names}"
