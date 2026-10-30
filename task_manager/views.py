from rest_framework import generics, status
from django.db.models import Count
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer

class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        total_tasks = Task.objects.count()

        serializer = TaskSerializer(tasks, many=True)
        return Response({
            'total_tasks': total_tasks,
            'tasks': serializer.data,
        })


class TaskDetailView(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task,pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


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