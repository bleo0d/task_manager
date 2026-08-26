import os
import django
from datetime import timedelta
from django.utils import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from task_manager.models import  Task, SubTask
task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=3),
)


SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=2),
    task=task
)


SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=timezone.now() + timedelta(days=1),
    task=task
)

tasks = Task.objects.filter(status="New")
for task in tasks:
    print(task)

subtasks = SubTask.objects.filter(status="Done", deadline__lt=timezone.now())
for subtask in subtasks:
    print(subtask)

Task.objects.filter(title="Prepare presentation").update(status="In progress")

SubTask.objects.filter(title="Gather information").update(deadline=timezone.now() - timedelta(days=2))

SubTask.objects.filter(title="Create slides").update(description="Create and format presentation slides")

Task.objects.filter(title="Prepare presentation").delete()



print(task.title)
print(task.description)
print(task.status)
print(task.deadline)
SubTask.objects.filter(task=task)
