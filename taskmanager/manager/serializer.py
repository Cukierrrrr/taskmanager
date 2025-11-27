from rest_framework.exceptions import PermissionDenied

from manager.models import Task, TaskGroup
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class TaskGroupBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ["id", "name", "description", "completion_percentage"]


class TaskReadBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name", "status", "description", "assigned_user", "creating_user"]


class TaskReadSerializer(TaskReadBaseSerializer):
    assigned_user = UserSerializer()
    creating_user = UserSerializer()
    group = TaskGroupBaseSerializer()

    class Meta(TaskReadBaseSerializer.Meta):
        fields = TaskReadBaseSerializer.Meta.fields + ["group"]


class TaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name", "status", "description", "assigned_user", "creating_user", "group"]
        read_only_fields = ["creating_user"]

    def add_user_to_group(self, task):
        if task.assigned_user is not None:
            group = TaskGroup.objects.get(id=task.group.id)
            if not group.assigned_users.filter(id=task.assigned_user.id).exists():
                group.assigned_users.add(task.assigned_user)
                group.save()

    def is_user_in_group(self, group_id, user):
        group = TaskGroup.objects.get(id=group_id)
        if group.assigned_users.filter(id=user.id).exists():
            return True
        return False

    def validate(self, validated_data):
        user = self.context["request"].user
        name = validated_data.get("name")
        group = validated_data.get("group")
        request_method = self.context.get("request").method
        if request_method in (
            "POST",
            "PUT",
        ) and (name is None or group is None):
            raise serializers.ValidationError("Name and Group fields are required")
        elif group and not (user.is_superuser or self.is_user_in_group(group.id, user)):
            raise PermissionDenied("You don't have permission to assign task to this group")

        return validated_data

    def create(self, validated_data):
        validated_data["creating_user"] = self.context["request"].user
        task = super().create(validated_data)
        self.add_user_to_group(task)
        return task

    def update(self, task, validated_data):
        task = super().update(task, validated_data)
        self.add_user_to_group(task)
        return task


class TaskHistoryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task.history.model
        fields = ["id", "name", "status", "description", "assigned_user", "group"]


class TaskHistorySerializer(TaskHistoryBaseSerializer):
    class Meta(TaskHistoryBaseSerializer.Meta):
        fields = ["history_id", "history_date"] + TaskHistoryBaseSerializer.Meta.fields


class TaskGroupReadSerializer(TaskGroupBaseSerializer):
    assigned_users = UserSerializer(many=True)
    assigned_tasks = TaskReadBaseSerializer(many=True)

    class Meta(TaskGroupBaseSerializer.Meta):
        fields = TaskGroupBaseSerializer.Meta.fields + ["assigned_users", "assigned_tasks"]


class TaskGroupWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ["id", "name", "description", "assigned_users"]
