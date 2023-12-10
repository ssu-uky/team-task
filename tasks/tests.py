import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from tasks.models import Task, SubTask, Team

client = APIClient()


@pytest.fixture()
def create_user(django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser",
        password="test123",
        team=User.TeamChoices.Danbi,
    )
    return user


@pytest.fixture()
def create_task(create_user):
    task = Task.objects.create(
        title="Test Task",
        content="Test Content",
        create_user=create_user,
    )
    return create_user, task


# Task testcode


@pytest.mark.django_db
def test_create_task_success(create_user):
    """
    일정 생성 성공 테스트
    """
    client.login(username="testuser", password="test123")
    url = reverse("task-create")
    data = {
        "title": "새 일정",
        "content": "일정 내용",
    }
    response = client.post(url, data, format="json")
    assert Task.objects.count() == 1
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.filter(title="새 일정").exists()


@pytest.mark.django_db
def test_create_task_unauthenticated(create_user):
    """
    비로그인 상태에서의 일정 생성 실패 테스트
    """
    url = reverse("task-create")
    data = {
        "title": "새 일정",
        "content": "일정 내용",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_create_task_fail(create_user, client):
    """
    필요한 데이터가 누락되어 일정 생성이 실패하는 경우
    """
    client.login(username="testuser", password="test123")
    url = reverse("task-create")
    incomplete_data = {"title": "불완전한 일정"}
    response = client.post(url, incomplete_data, format="json")
    assert Task.objects.count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_my_task_list_view(create_user):
    """
    내 팀의 일정 및 서브태스크 리스트 조회 테스트
    """
    client.login(username="testuser", password="test123")
    url = reverse("task-team-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "tasks" in response.data
    assert "subtasks" in response.data


@pytest.mark.django_db
def test_task_list_view(create_user):
    """
    모든 팀의 일정 리스트 조회 테스트
    """
    client.login(username="testuser", password="test123")
    url = reverse("task-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_task_detail_view_get(create_task):
    """
    일정 상세 정보 조회 테스트
    """
    _, task = create_task
    url = reverse("task-detail", args=[task.pk])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["task"]["title"] == task.title
    assert response.data["task"]["content"] == task.content


@pytest.mark.django_db
def test_task_detail_view_put(create_task, create_user):
    """
    일정 수정 테스트
    """
    _, task = create_task
    client.login(username="testuser", password="test123")
    url = reverse("task-detail", args=[task.pk])
    updated_data = {"title": "Updated Task"}
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == "Updated Task"


@pytest.mark.django_db
def test_task_owner_only(create_task):
    """
    일정 수정 권한이 없는 유저가 수정을 시도하는 경우
    """
    _, task = create_task
    new_user = User.objects.create_user(
        username="otheruser",
        password="otherpass",
    )
    client.login(username="otheruser", password="otherpass")
    url = reverse("task-detail", args=[task.pk])
    updated_data = {"title": "Updated Task"}
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_task_detail_view_delete(create_task, create_user):
    """
    일정 삭제 테스트
    """
    _, task = create_task
    client.login(username="testuser", password="test123")
    url = reverse("task-detail", args=[task.pk])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(pk=task.pk).exists()


@pytest.mark.django_db
def test_task_owner_delete(create_task):
    """
    일정 삭제 권한이 없는 유저가 삭제를 시도하는 경우
    """
    _, task = create_task
    new_user = User.objects.create_user(
        username="otheruser",
        password="otherpass",
    )
    client.login(username="otheruser", password="otherpass")
    url = reverse("task-detail", args=[task.pk])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


# SubTask testcode
@pytest.fixture()
def create_teams(django_user_model):
    team_objects = {}
    for team_name in User.TeamChoices.values:
        team, created = Team.objects.get_or_create(name=team_name)
        team_objects[team_name] = team
    return team_objects


@pytest.fixture()
def create_task_with_user(django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser2",
        password="testpassword2",
        team=User.TeamChoices.Danbi,
    )
    task = Task.objects.create(
        title="Task for SubTask",
        content="Task Content",
        create_user=user,
    )
    return user, task
