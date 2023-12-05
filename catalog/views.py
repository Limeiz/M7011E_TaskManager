from rest_framework import viewsets, status, permissions, authentication
from rest_framework.response import Response
from .serializers import UserSerializer, TaskSerializer, ListSerializer, ReminderSerializer
from .models import Task, List, Reminder
from django.contrib.auth.models import User


class IsAdmin(permissions.BasePermission):
    message = "You have to be an admin to view this content."

    def has_permission(self, request, view):
        group_name = "Admin"
        return request.user.groups.filter(name=group_name).exists()


class IsRegularUser:
    message = "You are not authorized."

    def has_permission(self, request, view):
        group_name = "RegularUser"
        return request.user.groups.filter(name=group_name).exists()


class CheckFunctions():
    def get_all_user_tasks(self, user):
        lists = List.objects.filter(assigned_users=user)
        all_user_tasks = Task.objects.none()

        for list_instance in lists:
            user_tasks = list_instance.get_user_tasks(user)
            all_user_tasks |= user_tasks

        return all_user_tasks.order_by('task_id')

    def user_has_task(self, user, task):
        if task in CheckFunctions.get_all_user_tasks(self, user):
            return True
        else:
            return False

    def user_has_reminder(self, user, reminder_id):
        reminder = Reminder.objects.get(reminder_id=reminder_id)
        if reminder.username == user:
            return True
        else:
            return False


class UserAdminViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def list(self, request):  # /api/users
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  # /api/users/<str:id>
        user = User.objects.get(user_id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/users/<str:id>
        user = User.objects.get(user_id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = User.objects.get(user_id=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        user = User.objects.get(user_id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskAdminViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def list(self, request):  # /api/tasks
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  # /api/tasks/<str:id>
        task = Task.objects.get(task_id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        task = Task.objects.get(task_id=pk)
        serializer = TaskSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        task = Task.objects.get(task_id=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskUserViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def list(self, request):  # /api/usertasks
        all_user_tasks = CheckFunctions.get_all_user_tasks(self, request.user)
        serializer = TaskSerializer(all_user_tasks, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/usertasks/<str:id>
        task = Task.objects.get(task_id=pk)
        if CheckFunctions.user_has_task(self, request.user, task):
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        else:
            message = "You can't view this task."
            return Response(message, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        task = Task.objects.get(task_id=pk)
        if CheckFunctions.user_has_task(self, request.user, task):
            serializer = TaskSerializer(instance=task, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            message = "You can't change this task."
            return Response(message, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        task = Task.objects.get(task_id=pk)
        if CheckFunctions.user_has_task(self, request.user, task):
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            message = "You can't delete this task."
            return Response(message, status=status.HTTP_204_NO_CONTENT)


class ReminderAdminViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def list(self, request):  # /api/reminders
        reminders = Reminder.objects.all()
        serializer = ReminderSerializer(reminders, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/reminders/<str:id>
        reminder = Reminder.objects.get(reminder_id=pk)
        serializer = ReminderSerializer(reminder)
        return Response(serializer.data)

    def update(self, request, pk=None):
        reminder = Reminder.objects.get(reminder_id=pk)
        serializer = ReminderSerializer(instance=reminder, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        reminder = Reminder.objects.get(reminder_id=pk)
        reminder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReminderViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]

    def create(self, request):
        serializer = ReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/reminders/<str:id>
        if CheckFunctions.user_has_reminder(self, request.user, pk):
            reminder = Reminder.objects.get(reminder_id=pk)
            serializer = ReminderSerializer(reminder)
            return Response(serializer.data)
        else:
            message = "You can't view this reminder"
            return Response(message, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        if CheckFunctions.user_has_reminder(self, request.user, pk):
            reminder = Reminder.objects.get(reminder_id=pk)
            serializer = ReminderSerializer(instance=reminder, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            message = "You can't update this reminder"
            return Response(message, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        if CheckFunctions.user_has_reminder(self, request.user, pk):
            reminder = Reminder.objects.get(reminder_id=pk)
            reminder.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            message = "You can't delete this reminder"
            return Response(message, status=status.HTTP_204_NO_CONTENT)


class ListViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def list(self, request):  # /api/lists
        lists = List.objects.all()
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/lists/<str:id>
        list = List.objects.get(list_id=pk)
        serializer = ListSerializer(list)
        return Response(serializer.data)

    def update(self, request, pk=None):
        list = List.objects.get(list_id=pk)
        serializer = ListSerializer(instance=list, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        list = List.objects.get(list_id=pk)
        list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
