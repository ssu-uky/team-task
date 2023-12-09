from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Task
from .serializers import (
    CreateTaskSerializer,
    TaskSerializer,
    TinyTaskSerializer,
    SubTaskSerializer,
    NewSubTaskSerializer,
    TinySubTaskSerializer,
)


class CreateTaskView(APIView):
    """
    일정 생성 API
    POST /api/v1/tasks/create/
    """

    def get(self, request):
        return Response(
            {"message": "title과 content를 입력해주세요."},
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
            "create_user": request.user,
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
    일정 상세 정보 API
    GET, PUT, DELETE /api/v1/tasks/<int:task_pk>/
    """

    # permission_classes = [IsAuthenticated]

    def get_object(self, task_pk):
        try:
            return Task.objects.get(pk=task_pk)
        except Task.DoesNotExist:
            raise NotFound("게시글을 찾을 수 없습니다.")

    def get(self, request, task_pk):
        task = self.get_object(task_pk)
        serializer = TaskSerializer(task)

        subtasks = task.subtasks.all()
        subtask_serializer = SubTaskSerializer(subtasks, many=True)

        return Response(
            {
                "task": serializer.data,
                "subtask": subtask_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, task_pk):
        task = self.get_object(task_pk)

        if request.user != task.create_user:
            return Response(
                {"message": "작성자만 수정할 수 있습니다."},
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

    def delete(self, request, task_pk):
        task = self.get_object(task_pk)

        # if task.is_complete:
        #     return Response(
        #         {"message": "완료된 일정은 삭제할 수 없습니다."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        if request.user != task.create_user:
            return Response(
                {"message": "작성자만 삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.delete()
        return Response(
            {"message": "삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )


class NewSubTaskView(APIView):
    """
    subtask 생성 API
    POST /api/v1/tasks/<int:task_pk>/subtasks/new/
    """
    def get_object(self, task_pk):
        try:
            return Task.objects.get(pk=task_pk)
        except:
            raise NotFound("게시글을 찾을 수 없습니다.")

    def get(self, request, task_pk):
        task = self.get_object(task_pk)
        serializer = TinyTaskSerializer(task)
        message = "sub_title, sub_content, team을 입력해주세요."
        return Response(
            {
                "task": serializer.data,
                "message": message,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, task_pk):
        task = self.get_object(task_pk)

        if request.user.team != task.create_user.team:
            return Response(
                {"message": "팀원만 등록할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        subtask_data = {
            "subtask_pk": request.data.get("pk"),
            "sub_title": request.data.get("sub_title"),
            "sub_content": request.data.get("sub_content"),
            "team": request.data.get("team"),
        }

        serializer = NewSubTaskSerializer(data=subtask_data)

        if serializer.is_valid():
            serializer.save(task=task)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SubTaskListView(APIView):
    """
    task_pk에 해당하는 subtask 리스트 API
    GET /api/v1/tasks/<int:task_pk>/subtasks/
    """
    
    def get_object(self, task_pk):
        try:
            return Task.objects.get(pk=task_pk)
        except:
            raise NotFound("게시글을 찾을 수 없습니다.")

    def get(self, request, task_pk):
        task = self.get_object(task_pk)
        subtasks = task.subtasks.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SubTaskDetailView(APIView):
    """
    subtask 상세 정보 API
    GET, PUT, DELETE /api/v1/tasks/<int:task_pk>/subtasks/<int:subtask_pk>/
    """

    def get_object(self, task_pk, subtask_pk):
        try:
            return Task.objects.get(pk=task_pk).subtasks.get(pk=subtask_pk)
        except:
            raise NotFound("게시글을 찾을 수 없습니다.")

    def get(self, request, task_pk, subtask_pk):
        subtask = self.get_object(task_pk, subtask_pk)
        serializer = SubTaskSerializer(subtask)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, task_pk, subtask_pk):
        subtask = self.get_object(task_pk, subtask_pk)

        if request.user != subtask.task.create_user:
            return Response(
                {"message": "작성자만 수정할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SubTaskSerializer(
            subtask,
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

    def delete(self, request, task_pk, subtask_pk):
        subtask = self.get_object(task_pk, subtask_pk)

        if request.user != subtask.task.create_user:
            return Response(
                {"message": "작성자만 삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        subtask.delete()
        return Response(
            {"message": "삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )