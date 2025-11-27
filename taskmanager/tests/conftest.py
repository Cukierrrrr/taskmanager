import pytest
from rest_framework.test import APIClient
from manager.models import Task, TaskGroup
from django.contrib.auth.models import User


@pytest.fixture
def user_fixture():
    return [
        User.objects.create_user(username="user1", password="password", id=501),
        User.objects.create_user(username="user2", password="password", id=502),
    ]


@pytest.fixture
def api_client(user_fixture):
    client1 = APIClient()
    client2 = APIClient()
    client1.force_authenticate(user=user_fixture[0])
    client2.force_authenticate(user=user_fixture[1])
    return [client1, client2]


@pytest.fixture
def task_group_fixture(user_fixture):
    taskGroup = TaskGroup.objects.bulk_create(
        [
            TaskGroup(name="Test Group", description="This is a test group", id=501),
            TaskGroup(name="Test Group2", description="This is a test group2", id=502),
        ]
    )
    taskGroup[0].assigned_users.add(user_fixture[0])
    taskGroup[1].assigned_users.add(user_fixture[0])
    taskGroup[1].assigned_users.add(user_fixture[1])
    return taskGroup


@pytest.fixture
def task_fixture(user_fixture, task_group_fixture):
    task1 = Task.objects.create(
        name="Test Task",
        status="R",
        description="This is a test task.",
        group=task_group_fixture[0],
        assigned_user=user_fixture[0],
        id=501,
        creating_user=user_fixture[0],
    )
    task2 = Task.objects.create(
        name="Test Task2",
        status="N",
        description="This is a test task2.",
        group=task_group_fixture[0],
        assigned_user=user_fixture[0],
        id=502,
        creating_user=user_fixture[0],
    )
    return [task1, task2]
