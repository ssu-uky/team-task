from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("myteam/", views.MyTaskListView.as_view(), name="task-team-list"),
    path("create/", views.CreateTaskView.as_view(), name="task-create"),
    path("<int:task_pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("<int:task_pk>/subtasks/", views.SubTaskListView.as_view(), name="subtask-list"),
    path(
        "<int:task_pk>/subtasks/new/", views.NewSubTaskView.as_view(), name="new-subtask"
    ),
    path("<int:task_pk>/subtasks/<int:subtask_pk>/", views.SubTaskDetailView.as_view(), name="subtask-detail"),
]