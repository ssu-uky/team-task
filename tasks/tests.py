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


@pytest.fixture()
def create_task_with_user(django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser2",
        password="testpassword2",
        team=User.TeamChoices.Danbi,
    )
    task = Task.objects.create(
        title="Task 제목",
        content="Task 내용",
        create_user=user,
    )

    team_values = [User.TeamChoices.Danbi.value, User.TeamChoices.Supie.value]

    subtask = SubTask.objects.create(
        sub_title="SubTask 제목",
        sub_content="SubTask 내용",
        task=task,
        subtask_create_user=user,
    )
    subtask.team.set(team_values)

    return user, task, subtask


@pytest.fixture()
def subtask_with_user(django_user_model):
    user = django_user_model.objects.create_user(
        username="subtaskuser",
        password="subtask123",
        team=User.TeamChoices.Danbi,
    )
    task = Task.objects.create(
        title="Task 제목",
        content="Task 내용",
        create_user=user,
    )

    team_danbi, _ = Team.objects.get_or_create(name=User.TeamChoices.Danbi)
    team_supie, _ = Team.objects.get_or_create(name=User.TeamChoices.Supie)
    team_values = [team_danbi.id, team_supie.id]

    subtask = SubTask.objects.create(
        sub_title="SubTask 제목",
        sub_content="SubTask 내용",
        task=task,
        subtask_create_user=user,
    )
    subtask.team.set(team_values)

    return user, task, subtask


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


@pytest.mark.django_db
def test_new_subtask_view_get_success(create_task):
    """
    존재하는 태스크에 대한 GET 요청 테스트
    """
    _, task = create_task
    url = reverse("new-subtask", args=[task.pk])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "task" in response.data
    assert "message" in response.data


@pytest.mark.django_db
def test_new_subtask_view_get_not_found():
    """
    존재하지 않는 태스크에 대한 GET 요청 테스트
    """
    url = reverse("new-subtask", args=[999])  # 존재하지 않는 task_pk
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_new_subtask_view_post_success(subtask_with_user):
    """
    같은 팀 사용자에 의한 POST 요청 성공 테스트
    """
    user, task, subtask = subtask_with_user
    client.login(username="subtaskuser", password="subtask123")
    url = reverse("new-subtask", args=[task.pk])

    team_names = [team.name for team in subtask.team.all()]
    print("팀 이름:", team_names)

    data = {
        "sub_title": "새 서브태스크",
        "sub_content": "새 서브태스크 내용",
        "team": team_names,
    }
    response = client.post(url, data, format="json")
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert SubTask.objects.filter(sub_title="새 서브태스크").exists()


@pytest.mark.django_db
def test_new_subtask_view_post_forbidden(subtask_with_user, django_user_model):
    """
    다른 팀 사용자에 의한 POST 요청 실패 테스트
    """
    user, task, subtask = subtask_with_user
    other_user = django_user_model.objects.create_user(
        username="otheruser", password="otherpass", team="OtherTeam"
    )
    client.login(username="otheruser", password="otherpass")
    url = reverse("new-subtask", args=[task.pk])
    data = {
        "sub_title": "새 서브태스크",
        "sub_content": "새 서브태스크 내용",
        "team": ["OtherTeam"],
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_new_subtask_view_post_bad_request(create_task):
    """
    필수 데이터 누락으로 인한 POST 요청 실패 테스트
    """
    _, task = create_task
    client.login(username="testuser", password="test123")
    url = reverse("new-subtask", args=[task.pk])
    data = {
        "sub_title": "새 서브태스크",
        # sub_content 누락
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_new_subtask_view_post_not_found():
    """
    존재하지 않는 태스크에 대한 POST 요청 테스트
    """
    client.login(username="testuser", password="test123")
    url = reverse("new-subtask", args=[999])  # 존재하지 않는 task_pk
    data = {"sub_title": "새 서브태스크", "sub_content": "서브태스크 내용", "team": ["SomeTeam"]}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_subtask_detail_view_get_success(subtask_with_user):
    """
    존재하는 서브태스크에 대한 GET 요청 테스트
    """
    user, task, subtask = subtask_with_user
    client.login(username="subtaskuser", password="subtask123")
    url = reverse("subtask-detail", args=[task.pk, subtask.pk])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["sub_title"] == subtask.sub_title


@pytest.mark.django_db
def test_subtask_detail_view_get_not_found(subtask_with_user):
    """
    존재하지 않는 서브태스크에 대한 GET 요청 테스트
    """
    user, task, _ = subtask_with_user
    client.login(username="subtaskuser", password="subtask123")
    url = reverse("subtask-detail", args=[task.pk, 999])  # 존재하지 않는 subtask_pk
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_subtask_detail_view_put_success(subtask_with_user):
    """
    서브태스크 수정 테스트
    """
    user, task, subtask = subtask_with_user
    client.login(username="subtaskuser", password="subtask123")
    url = reverse("subtask-detail", args=[task.pk, subtask.pk])
    updated_data = {"sub_title": "Updated SubTask"}
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    subtask.refresh_from_db()
    assert subtask.sub_title == "Updated SubTask"


@pytest.mark.django_db
def test_subtask_detail_view_put_forbidden(subtask_with_user, django_user_model):
    """
    detail put 권한 없는 유저가 수정을 시도하는 경우
    """
    user, task, subtask = subtask_with_user

    other_user = django_user_model.objects.create_user(
        username="otheruser", password="otherpass", team="OtherTeam"
    )
    client.login(username="otheruser", password="otherpass")
    url = reverse("subtask-detail", args=[task.pk, subtask.pk])
    updated_data = {"sub_title": "Updated SubTask"}
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_subtask_detail_view_delete_success(subtask_with_user):
    """
    서브태스크 삭제 테스트
    """
    user, task, subtask = subtask_with_user
    client.login(username="subtaskuser", password="subtask123")
    url = reverse("subtask-detail", args=[task.pk, subtask.pk])
    response = client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not SubTask.objects.filter(pk=subtask.pk).exists()
