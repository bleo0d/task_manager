from django.contrib import admin
from .models import Task, SubTask, Category


#

#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)


class Taskinline(admin.StackedInline):
    model = SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title','description','deadline','status')
    inlines = [Taskinline]

    @admin.display(description='название')
    def short_title(self, obj):
        if len(obj.title)>10:
            return obj.title[:10] + "..."
        return obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title','description','deadline','status')
    actions = ['make_done']

    @admin.action(description='готово')
    def make_done(self, request, queryset):
        queryset.update(status="done")




