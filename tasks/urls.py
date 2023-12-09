from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateTaskView.as_view(), name="task-create"),
    path("list/", views.TaskListView.as_view(), name="task-list"),
    path("list/team/", views.MyTaskListView.as_view(), name="task-team-list"),
    path("<int:task_pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("<int:task_pk>/subtasks/", views.SubTaskListView.as_view(), name="subtask-list"),
    path(
        "<int:task_pk>/subtasks/new/", views.NewSubTaskView.as_view(), name="new-subtask"
    ),
    path("<int:task_pk>/subtasks/<int:subtask_pk>/", views.SubTaskDetailView.as_view(), name="subtask-detail"),
]
