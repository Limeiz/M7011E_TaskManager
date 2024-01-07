from rest_framework import permissions, authentication, \
    generics

from .models import Task, List, Reminder
from .serializers import TaskSerializer, ListSerializer, \
    ReminderSerializer


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


class TaskViewSet(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.TokenAuthentication]


class TaskAdminListCreate(TaskViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class TaskAdminGetUpdateDelete(TaskViewSet,
                               generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'slug'


class TaskUserListCreate(TaskViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class TaskUserGetUpdateDelete(TaskViewSet,
                              generics.RetrieveUpdateDestroyAPIView):
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


class ReminderAdminGetUpdateDelete(ReminderViewSet,
                                   generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'slug'


class ReminderUserListCreate(ReminderViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Reminder.objects.filter(username=self.request.user)


class ReminderUserGetUpdateDelete(ReminderViewSet,
                                  generics.RetrieveUpdateDestroyAPIView):
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


class ListAdminGetUpdateDelete(ListViewSet,
                               generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'slug'


class ListUserListCreate(ListViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return List.objects.filter(assigned_users=self.request.user)


class ListUserGetUpdateDelete(ListViewSet,
                              generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]
    lookup_field = 'slug'

    def get_queryset(self):
        return List.objects.filter(assigned_users=self.request.user)
