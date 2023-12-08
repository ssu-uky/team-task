from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Task
from .serializers import CreateTaskSerializer, TaskSerializer


class CreateTaskView(APIView):
    """
    일정 생성 API
    POST /api/v1/tasks/create/
    """

    def get(self, request):
        return Response(
            {"message": " title과 content를 입력해주세요."},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "로그인이 필요합니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        create_task = {
            "task_pk": request.data.get("pk"),
            "create_user": request.user.username,
            "team": request.user.team,
            "title": request.data.get("title"),
            "content": request.data.get("content"),
        }

        serializer = CreateTaskSerializer(data=create_task)
        if serializer.is_valid():
            serializer.save(create_user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class MyTaskListView(APIView):
    """
    내가 포함 된 팀의 일정 리스트 API
    GET /api/v1/tasks/list/team/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(create_user__team=request.user.team)
        serializer = TaskSerializer(tasks, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class TaskListView(APIView):
    """
    일정 리스트 API (팀 이름으로 팀 별 일정 리스트 검색 가능)
    GET /api/v1/tasks/list/ : 모든 팀의 일정 리스트
    GET api/v1/tasks/list/?team=팀이름 : 검색한 팀 이름의 일정 리스트
    """

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        team_name = request.query_params.get("team")

        if team_name:
            tasks = Task.objects.filter(create_user__team=team_name)
        else:
            tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class TaskDetailView(APIView):
    """
    일정 상세 정보 API :: GET, PUT, DELETE
    /api/v1/tasks/<int:pk>/
    """

    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound("게시글을 찾을 수 없습니다.")

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        task = self.get_object(pk)

        if request.user != task.create_user:
            return Response(
                {"message": "생성자만 수정할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        task = self.get_object(pk)

        # if task.is_complete:
        #     return Response(
        #         {"message": "완료된 일정은 삭제할 수 없습니다."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        if request.user != task.create_user:
            return Response(
                {"message": "생성자만 삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.delete()
        return Response(
            {"message": "삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )
