from rest_framework import generics, status
from django.db.models import Count
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .pagination import TaskPagination
from django.utils import timezone
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


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
        day_of_week = request.query_params.get('day_of_week')
        tasks = Task.objects.all()

        if day_of_week:
            days = {
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6,
            }
            day = days.get(day_of_week.lower())
            if day is None:
                return Response({'error': 'Invalid day of week'

                }, status=status.HTTP_400_BAD_REQUEST)
            tasks = [task for task in tasks if task.deadline.weekday() == day]

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

class SubTaskListCreateView(APIView):
    def get(self, request):
        tasks = SubTask.objects.all().order_by('-created_at')

        task_title = request.query_params.get('task_title')
        status = request.query_params.get('status')
        if task_title:
            tasks = tasks.filter(task__title=task_title)

        if status:
            tasks = tasks.filter(status=status)

        paginator = TaskPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request)

        serializer = SubTaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        task = get_object_or_404(SubTask,pk=pk)
        serializer = SubTaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(SubTask,pk=pk)
        serializer = SubTaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(SubTask,pk=pk)
        task.delete()
        return Response(
            {"message": "SubTask deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
