from django.shortcuts import render
from rest_framework import viewsets, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, TaskSerializer, ReminderSerializer, ListSerializer
from .models import User, Task, Reminder, List

class IsAdmin(permissions.BasePermission):
    message = "You have to be an admin to view this content."
    def has_permission(self, request, view):
        group_name = "Admin"
        return request.user.groups.filter(name=group_name).exists()
#Token c21d62f284a3c47ed9b176e6c81c76cdded4dd5f
#Admin Token 85f6b629fd2f2d34dffb8e399f8931a38b57c88d
class UserViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    def list(self, request):  # /api/users
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

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


class TaskViewSet(viewsets.ViewSet):
    def list(self, request):  # /api/tasks
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/tasks/<str:id>
        task = Task.objects.get(task_id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

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


class ReminderViewSet(viewsets.ViewSet):
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


class ListViewSet(viewsets.ViewSet):
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

