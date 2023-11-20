from django.contrib import admin
from django.urls import path

from .views import UserViewSet, TaskViewSet, ReminderViewSet

urlpatterns = [
    path('users', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('users/<str:pk>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('tasks', TaskViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('tasks/<str:pk>', TaskViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('reminders', ReminderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('reminders/<str:pk>', ReminderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }))

]