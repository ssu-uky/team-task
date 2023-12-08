from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import SignupSerializer


class SignUpView(APIView):
    """
    POST /api/v1/users/signup/
    """

    def get(self, request):
        return Response(
            {"message": "username, password, team을 입력해주세요"},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user_pk": user.pk,
                    "username": user.username,
                    "team": user.team,
                    "message": f"{user.team} 팀의 {user.username}님, 회원가입이 완료되었습니다.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/v1/users/login/
    """

    def get(self, request):
        return Response(
            {"message": "username, password를 입력해주세요"},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response(
                {"message": "username, password를 입력해주세요"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                {
                    "user_pk": user.pk,
                    "username": user.username,
                    "team": user.team,
                    "message": f"{user.team} 팀의 {user.username}님, 로그인되었습니다.",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "username 또는 password가 일치하지 않습니다."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    """
    POST /api/v1/users/logout/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"message": "로그아웃 하시겠습니까?"},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        logout(request)
        return Response(
            {"message": "로그아웃되었습니다."},
            status=status.HTTP_200_OK,
        )
