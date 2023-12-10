import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

client = APIClient()


@pytest.fixture()
def create_user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="test123",
        team=User.TeamChoices.Danbi,
    )


@pytest.mark.django_db
def test_signup_success(create_user):
    """
    유효한 팀 값으로 성공적인 회원가입 테스트
    """
    url = reverse("signup")
    data = {
        "username": "newuser",
        "password": "newpassword",
        "team": User.TeamChoices.Darae,
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 2
    assert User.objects.get(username="newuser").team == User.TeamChoices.Darae
    assert User.objects.filter(username="newuser").exists()
    assert (
        response.data["message"]
        == f"{data['team']} 팀의 {data['username']}님, 회원가입이 완료되었습니다."
    )


@pytest.mark.django_db
def test_signup_failure_invalid_team(create_user):
    """
    유효하지 않은 팀 값으로 인한 회원가입 실패 테스트
    """
    url = reverse("signup")
    data = {
        "username": "newuser",
        "password": "newpassword",
        "team": "InvalidTeam",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 1
    assert "team" in response.data


@pytest.mark.django_db
def test_login_success(create_user):
    """
    성공적인 로그인 테스트
    """
    url = reverse("login")
    data = {
        "username": "testuser",
        "password": "test123",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "testuser"
    assert response.data["team"] == User.TeamChoices.Danbi


@pytest.mark.django_db
def test_login_failure(create_user):
    """
    로그인 실패 테스트
    """
    url = reverse("login")
    data = {
        "username": "testuser",
        "password": "test123!", # 잘못된 비밀번호
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_logout(create_user):
    """
    로그아웃 테스트
    """
    client.login(
        username="testuser",
        password="test123",
    )
    url = reverse("logout")
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
