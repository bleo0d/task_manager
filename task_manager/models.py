from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Created at'))
    class Meta:
        abstract = True
class TaskStatus(models.TextChoices):
        NEW = "new", _("New")
        IN_PROGRESS = "in_progress", _("In Progress")
        PENDING = "pending", _("Pending")
        BLOCKED = "blocked", _("Blocked")
        DONE = "done", _("Done")



class Task(TimeStamp):
    title = models.CharField(unique=True, max_length=100, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    categories = models.ManyToManyField("Category", verbose_name=_('Categories'))
    status = models.CharField(choices=TaskStatus, max_length=20, verbose_name=_('Status'))
    deadline = models.DateTimeField(verbose_name=_('Deadline'))

    def __str__(self):
        return self.title

class SubTask(TimeStamp):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('Task'))
    status=models.CharField(choices=TaskStatus, max_length=20, verbose_name=_('Status'))
    deadline = models.DateTimeField(verbose_name=_('Deadline'))

    def __str__(self):
        return self.title

class Category(TimeStamp):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    def __str__(self):
        return self.name