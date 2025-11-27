from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from manager.models import Task, TaskGroup
from manager.serializer import (
    TaskReadSerializer,
    TaskWriteSerializer,
    TaskHistoryBaseSerializer,
    TaskHistorySerializer,
    TaskGroupReadSerializer,
    TaskGroupWriteSerializer,
)
from datetime import datetime, timedelta
from manager.permissions import TaskPermission, GroupPermission


class ChoicesView(APIView):
    permission_classes = (IsAuthenticated,)
    choices = []

    def get(self, request):
        return Response(
            [
                {"symbol": symbol, "nazwa": nazwa}
                for symbol, nazwa in sorted(self.choices, key=lambda x: x[1])
            ]
        )


class TaskGroupViewSet(viewsets.ModelViewSet):
    queryset = TaskGroup.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["id", "name"]
    permission_classes = [IsAuthenticated, GroupPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or self.action != "list":
            return TaskGroup.objects.all()
        return TaskGroup.objects.filter(assigned_users=user)

    def get_serializer_class(self):
        if self.action in (
            "create",
            "update",
            "partial_update",
        ):
            return TaskGroupWriteSerializer
        else:
            return TaskGroupReadSerializer

    @action(detail=True, methods=["post"], url_path="assign_user")
    def assign_user(self, request, pk):
        group = self.get_object()
        user_id = request.data.get("id")
        if not user_id:
            return Response({"error": "user id parameters is required."}, status=400)
        try:
            user = User.objects.get(id=user_id)
            group.assigned_users.add(user)
            return Response({"message": "user succesfuly assigned to group."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "No user found for the given ID"}, status=404)

    @action(detail=True, methods=["post"], url_path="unassign_user")
    def unassign_user(self, request, pk):
        group = self.get_object()
        user_id = request.data.get("id")
        if not user_id:
            return Response({"error": "user id parameters is required."}, status=400)
        try:
            user = User.objects.get(id=user_id)
            group.assigned_users.remove(user)
            return Response({"message": "user succesfuly deleted from group."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "No user found for the given ID"}, status=404)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["assigned_user", "creating_user", "group", "status"]
    search_fields = ["name", "description"]
    ordering_fields = ["id", "name", "status", "assigned_user", "creating_user", "group"]
    permission_classes = [IsAuthenticated, TaskPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or self.action != "list":
            return Task.objects.all()
        return Task.objects.filter(group__assigned_users=user)

    def get_serializer_class(self):
        if self.action in (
            "create",
            "update",
            "partial_update",
        ):
            return TaskWriteSerializer
        else:
            return TaskReadSerializer

    @action(detail=False, methods=["get"], url_path="history")
    def history(self, request):
        user = request.user
        history = Task.history.filter(group__assigned_users=user)
        task_id = request.query_params.get("id")
        if task_id:
            history = history.filter(id=task_id)
        date_filter = request.query_params.get("date")
        if date_filter:
            try:
                date_filter = datetime.fromisoformat(date_filter)
                history = history.filter(
                    history_date__gte=date_filter, history_date__lt=date_filter + timedelta(days=1)
                )
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        serializer = TaskHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="task_at_time")
    def task_at_time(self, request):
        task_id = request.query_params.get("id")
        date = request.query_params.get("date")
        user = request.user
        if not task_id or not date:
            return Response({"error": "id and date parameters are required."}, status=400)
        if Task.objects.filter(id=task_id, group__assigned_users=user).count() == 0:
            return Response(
                {"error": "you don't have permission to see history of this task."}, status=403
            )
        try:
            date = datetime.fromisoformat(date)
            date = date.replace(hour=23, minute=59, second=59)
            history_entry = (
                Task.history.filter(id=task_id, history_date__lte=date)
                .order_by("-history_date")
                .first()
            )
            if history_entry:
                serializer = TaskHistoryBaseSerializer(history_entry)
                return Response(serializer.data)
            else:
                return Response({"error": "No task found for the given ID and date."}, status=404)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
