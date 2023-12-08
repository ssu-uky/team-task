from django.db import models

from users.models import User


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
