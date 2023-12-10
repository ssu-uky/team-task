from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("create/", views.CreateTaskView.as_view(), name="task-create"),
    path("myteam/", views.MyTaskListView.as_view(), name="task-team-list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
]
