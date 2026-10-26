from rest_framework import generics
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        total_tasks = Task.objects.count()

        status_counts = tasks.values('status').annotate(Count('status')).order_by('-status')

        overdue_tasks = tasks.filter(deadline__lt=timezone.now()).exclude(status='completed').count()

        return Response({
            'total_tasks': total_tasks,
            'status_counts': status_counts,
            'overdue_tasks': overdue_tasks,
        })