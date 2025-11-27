import pytest
from rest_framework import status
from unittest.mock import ANY
from django.urls import reverse

TASK_GROUP_DATA = [
    {
        "id": 501,
        "name": "Test Group",
        "description": "This is a test group",
        "assigned_tasks": [],
        "assigned_users": [{"username": "user1"}],
        "completion_percentage": "100%",
    },
    {
        "id": 502,
        "name": "Test Group2",
        "description": "This is a test group2",
        "assigned_tasks": [],
        "assigned_users": [{"username": "user1"}, {"username": "user2"}],
        "completion_percentage": "100%",
    },
]


@pytest.mark.django_db
def test_task_group_post(api_client):
    response = api_client[0].post(
        reverse(
            "taskgroup-list",
        ),
        data={
            "name": "Test Group2",
            "description": "This is a test group2",
            "assigned_users": [],
        },
    )
    assert (response.status_code, response.json()) == (
        status.HTTP_201_CREATED,
        {
            "id": ANY,
            "name": "Test Group2",
            "description": "This is a test group2",
            "assigned_users": [],
        },
    )


@pytest.mark.django_db
def test_task_group_list(task_group_fixture, api_client):
    response = api_client[0].get(
        reverse(
            "taskgroup-list",
        )
    )
    assert (response.status_code, response.json()) == (status.HTTP_200_OK, TASK_GROUP_DATA)


@pytest.mark.django_db
def test_task_group_list_permission(task_group_fixture, api_client):
    response = api_client[1].get(
        reverse(
            "taskgroup-list",
        )
    )
    assert (response.status_code, response.json()) == (status.HTTP_200_OK, [TASK_GROUP_DATA[1]])


@pytest.mark.django_db
def test_task_group_detail(task_group_fixture, api_client):
    response = api_client[0].get(
        reverse("taskgroup-detail", kwargs={"pk": task_group_fixture[0].id})
    )
    assert (response.status_code, response.json()) == (status.HTTP_200_OK, TASK_GROUP_DATA[0])


@pytest.mark.django_db
def test_task_group_detail_permission(task_group_fixture, api_client):
    response = api_client[1].get(
        reverse("taskgroup-detail", kwargs={"pk": task_group_fixture[0].id})
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_group_patch(task_group_fixture, api_client, user_fixture):
    response = api_client[0].patch(
        reverse("taskgroup-detail", kwargs={"pk": task_group_fixture[0].id}),
        data={"name": "Updated Test Group"},
    )
    assert (
        response.status_code,
        response.json() | {"assigned_tasks": ANY, "completion_percentage": ANY},
    ) == (
        status.HTTP_200_OK,
        TASK_GROUP_DATA[0] | {"name": "Updated Test Group", "assigned_users": [user_fixture[0].id]},
    )


@pytest.mark.django_db
def test_task_group_patch_permission(task_group_fixture, api_client):
    response = api_client[1].patch(
        reverse("taskgroup-detail", kwargs={"pk": task_group_fixture[0].id}),
        data={"name": "Updated Test Group"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_group_delete(task_group_fixture, api_client):
    response = api_client[0].delete(
        reverse("taskgroup-detail", kwargs={"pk": task_group_fixture[0].id}),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_task_group_delete_permission(task_group_fixture, api_client):
    response = api_client[1].delete(
        reverse("taskgroup-detail", kwargs={"pk": task_group_fixture[0].id}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_group_assign_user(task_group_fixture, api_client, user_fixture):
    response = api_client[0].post(
        reverse("taskgroup-assign-user", kwargs={"pk": task_group_fixture[0].id}),
        data={"id": user_fixture[1].id},
    )
    assert (
        response.status_code,
        task_group_fixture[0].assigned_users.filter(id=user_fixture[1].id).exists(),
    ) == (status.HTTP_200_OK, True)


@pytest.mark.django_db
def test_task_group_unassign_user(task_group_fixture, api_client, user_fixture):
    response = api_client[0].post(
        reverse("taskgroup-unassign-user", kwargs={"pk": task_group_fixture[0].id}),
        data={"id": user_fixture[0].id},
    )
    assert (
        response.status_code,
        task_group_fixture[0].assigned_users.filter(id=user_fixture[0].id).exists(),
    ) == (status.HTTP_200_OK, False)


@pytest.mark.django_db
def test_task_group_assign_user_permission(task_group_fixture, api_client, user_fixture):
    response = api_client[1].post(
        reverse("taskgroup-assign-user", kwargs={"pk": task_group_fixture[0].id}),
        data={"id": user_fixture[1].id},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_group_unassign_user_permission(task_group_fixture, api_client, user_fixture):
    response = api_client[1].post(
        reverse("taskgroup-unassign-user", kwargs={"pk": task_group_fixture[0].id}),
        data={"id": user_fixture[0].id},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
