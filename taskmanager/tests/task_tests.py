from datetime import datetime

import pytest
from rest_framework import status
from unittest.mock import ANY
from django.urls import reverse

TASK_DATA = [
    {
        "id": 501,
        "name": "Test Task",
        "status": "R",
        "description": "This is a test task.",
        "group": {
            "completion_percentage": "50.0%",
            "description": "This is a test group",
            "id": 501,
            "name": "Test Group",
        },
        "assigned_user": {"username": "user1"},
        "creating_user": {"username": "user1"},
    },
    {
        "id": 502,
        "name": "Test Task2",
        "status": "N",
        "description": "This is a test task2.",
        "group": {
            "completion_percentage": "50.0%",
            "description": "This is a test group",
            "id": 501,
            "name": "Test Group",
        },
        "assigned_user": {"username": "user1"},
        "creating_user": {"username": "user1"},
    },
]


@pytest.mark.django_db
def test_task_post(api_client, task_group_fixture, user_fixture):
    response = api_client[0].post(
        reverse(
            "task-list",
        ),
        data={
            "name": "Test Task2",
            "description": "This is a test task2",
            "status": "N",
            "group": task_group_fixture[0].id,
        },
    )
    assert (response.status_code, response.json()) == (
        status.HTTP_201_CREATED,
        {
            "id": ANY,
            "name": "Test Task2",
            "description": "This is a test task2",
            "status": "N",
            "group": task_group_fixture[0].id,
            "creating_user": user_fixture[0].id,
            "assigned_user": None,
        },
    )


@pytest.mark.django_db
def test_task_list(task_fixture, api_client):
    response = api_client[0].get(
        reverse(
            "task-list",
        )
    )
    assert (response.status_code, response.json()) == (status.HTTP_200_OK, TASK_DATA)


@pytest.mark.django_db
def test_task_list_permission(task_fixture, api_client):
    response = api_client[1].get(
        reverse(
            "task-list",
        )
    )
    assert (response.status_code, response.json()) == (status.HTTP_200_OK, [])


@pytest.mark.django_db
def test_task_detail(task_fixture, api_client):
    response = api_client[0].get(reverse("task-detail", kwargs={"pk": task_fixture[0].id}))
    assert (response.status_code, response.json()) == (status.HTTP_200_OK, TASK_DATA[0])


@pytest.mark.django_db
def test_task_detail_permission(task_fixture, api_client):
    response = api_client[1].get(reverse("task-detail", kwargs={"pk": task_fixture[0].id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_patch(task_fixture, api_client):
    response = api_client[0].patch(
        reverse("task-detail", kwargs={"pk": task_fixture[0].id}),
        data={"name": "Updated Test Task"},
    )
    assert (response.status_code, response.json()) == (
        status.HTTP_200_OK,
        TASK_DATA[0]
        | {
            "name": "Updated Test Task",
            "assigned_user": task_fixture[0].assigned_user.id,
            "creating_user": task_fixture[0].assigned_user.id,
            "group": task_fixture[0].group.id,
        },
    )


@pytest.mark.django_db
def test_task_patch_permission(task_fixture, api_client):
    response = api_client[1].patch(
        reverse("task-detail", kwargs={"pk": task_fixture[0].id}),
        data={"name": "Updated Test Task"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_delete(task_fixture, api_client):
    response = api_client[0].delete(
        reverse("task-detail", kwargs={"pk": task_fixture[0].id}),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_task_delete_permission(task_fixture, api_client):
    response = api_client[1].delete(
        reverse("task-detail", kwargs={"pk": task_fixture[0].id}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_history(task_fixture, api_client):
    response = api_client[0].get(reverse("task-history"), data={"id": task_fixture[0].id})
    assert (response.status_code, response.json()[0] | {"creating_user": ANY}) == (
        status.HTTP_200_OK,
        TASK_DATA[0]
        | {
            "history_date": ANY,
            "history_id": ANY,
            "assigned_user": task_fixture[0].assigned_user.id,
            "group": task_fixture[0].group.id,
        },
    )


@pytest.mark.django_db
def test_task_history_permission(task_fixture, api_client):
    response = api_client[1].get(reverse("task-history"), data={"id": task_fixture[0].id})
    assert (response.status_code, response.json()) == (status.HTTP_200_OK, [])


@pytest.mark.django_db
def test_task_at_time(task_fixture, api_client):
    response = api_client[0].get(
        reverse("task-task-at-time"), data={"id": task_fixture[0].id, "date": datetime.now().date()}
    )
    assert (response.status_code, response.json() | {"creating_user": ANY}) == (
        status.HTTP_200_OK,
        TASK_DATA[0]
        | {"assigned_user": task_fixture[0].assigned_user.id, "group": task_fixture[0].group.id},
    )


@pytest.mark.django_db
def test_task_at_time_permission(task_fixture, api_client):
    response = api_client[1].get(
        reverse("task-task-at-time"), data={"id": task_fixture[0].id, "date": datetime.now().date()}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
