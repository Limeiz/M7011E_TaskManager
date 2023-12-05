from django.contrib import admin
from django.urls import path

from .views import UserViewSet, TaskUserViewSet, TaskAdminViewSet, ListViewSet, ReminderViewSet, UserAdminViewSet, \
    ReminderAdminViewSet

urlpatterns = [
    path('users', UserViewSet.as_view({
        'post': 'create'
    })),
    path('users/<str:pk>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('usersadmin', UserAdminViewSet.as_view({
        'get': 'list'
    })),
    path('tasks', TaskAdminViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('tasks/<str:pk>', TaskAdminViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('usertasks', TaskUserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('usertasks/<str:pk>', TaskUserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('remindersadmin', ReminderAdminViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('remindersadmin/<str:pk>', ReminderAdminViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('reminders', ReminderViewSet.as_view({
        'post': 'create'
    })),
    path('reminders/<str:pk>', ReminderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('lists', ListViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('lists/<str:pk>', ListViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }))

]
