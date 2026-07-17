from django.contrib import admin
from .models import Task, SubTask, Category

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','description','deadline','status')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title','description','deadline','status')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


