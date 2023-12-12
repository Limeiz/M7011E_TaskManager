from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions, authentication, generics
from rest_framework.response import Response

from .models import Task, List, Reminder
from .serializers import UserSerializer, TaskSerializer, ListSerializer, ReminderSerializer

class IsAdmin(permissions.BasePermission):
    message = "You have to be an admin to view this content."

    def has_permission(self, request, view):
        group_name = "Admin"
        return request.user.groups.filter(name=group_name).exists()


class IsRegularUser(permissions.BasePermission):
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
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUserViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def update(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskViewSet(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.TokenAuthentication]

class TaskAdminListCreate(TaskViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class TaskAdminGetUpdateDelete(TaskViewSet, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'slug'

class TaskUserListCreate(TaskViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]
    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

class TaskUserGetUpdateDelete(TaskViewSet, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]
    lookup_field = 'slug'

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

class ReminderViewSet(generics.GenericAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    authentication_classes = [authentication.TokenAuthentication]

class ReminderAdminListCreate(ReminderViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class ReminderAdminGetUpdateDelete(ReminderViewSet, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'slug'

class ReminderUserListCreate(ReminderViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Reminder.objects.filter(username=self.request.user)
class ReminderUserGetUpdateDelete(ReminderViewSet, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]
    lookup_field = 'slug'

    def get_queryset(self):
        return Reminder.objects.filter(username=self.request.user)


class ListViewSet(generics.GenericAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    authentication_classes = [authentication.TokenAuthentication]
class ListAdminListCreate(ListViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
class ListAdminGetUpdateDelete(ListViewSet, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'slug'

class ListUserListCreate(ListViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return List.objects.filter(assigned_users=self.request.user)

class ListUserGetUpdateDelete(ListViewSet, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]
    lookup_field = 'slug'

    def get_queryset(self):
        return List.objects.filter(assigned_users=self.request.user)