from django.contrib import admin
from manager.models import Task, TaskGroup


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "assigned_user", "description")
    list_filter = ("status",)
    search_fields = ("id", "name", "description")
    ordering = ("id",)


@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name", "description")
    ordering = ("id",)
