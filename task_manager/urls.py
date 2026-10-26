from django.urls import path
from .views import TaskCreateView, TaskDetailView, TaskListView, TaskAPIView

urlpatterns = [
    path('tasks/create', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/statistic', TaskAPIView.as_view(), name='task-detail'),
]