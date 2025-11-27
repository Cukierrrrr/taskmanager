from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.db import models
from manager.choices import TaskStatus


class TaskGroup(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    assigned_users = models.ManyToManyField(User, related_name="task_groups", blank=True)

    @property
    def completion_percentage(self):
        tasks = list(self.assigned_tasks.values_list("status", flat=True))
        i = len(tasks)
        if i > 0:
            return f"{round((tasks.count('R') / i) * 100, 3)}%"
        else:
            return "100%"


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=1, choices=TaskStatus.choices, default=TaskStatus.NEW)
    description = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    assigned_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks"
    )
    creating_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, related_name="assigned_tasks")
