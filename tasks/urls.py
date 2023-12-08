from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateTaskView.as_view(), name="task-create"),
    path("list/", views.TaskListView.as_view(), name="task-list"),
    path("list/team/", views.MyTaskListView.as_view(), name="task-team-list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
]
