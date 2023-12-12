from django.urls import path

from .views import (UserViewSet, UserAdminViewSet,
                    TaskAdminListCreate, TaskAdminGetUpdateDelete,
                    TaskUserListCreate, TaskUserGetUpdateDelete,
                    ReminderAdminListCreate, ReminderUserListCreate,
                    ReminderUserGetUpdateDelete,
                    ReminderAdminGetUpdateDelete,
                    ListAdminListCreate, ListAdminGetUpdateDelete,
                    ListUserGetUpdateDelete, ListUserListCreate, )

urlpatterns = [
    path('users', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('usersadmin', UserAdminViewSet.as_view({
        'get': 'list'
    })),
    path('usersadmin/<str:pk>', UserAdminViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    path('tasks-admin', TaskAdminListCreate.as_view(), name='task_admin_list'),
    path('tasks-admin/<slug:slug>', TaskAdminGetUpdateDelete.as_view(),
         name='task_admin_details'),

    path('tasks-user', TaskUserListCreate.as_view(), name='task_user_list'),
    path('tasks-user/<slug:slug>', TaskUserGetUpdateDelete.as_view(),
         name='task_user_details'),

    path('reminders-admin', ReminderAdminListCreate.as_view(),
         name='reminder_admin_list'),
    path('reminders-admin/<slug:slug>', ReminderAdminGetUpdateDelete.as_view(),
         name='reminder_admin_details'),

    path('reminders-user', ReminderUserListCreate.as_view(),
         name='reminder_user_list'),
    path('reminders-user/<slug:slug>', ReminderUserGetUpdateDelete.as_view(),
         name='reminder_user_details'),

    path('list-admin', ListAdminListCreate.as_view(), name='list_admin_list'),
    path('list-admin/<slug:slug>', ListAdminGetUpdateDelete.as_view(),
         name='list_admin_details'),

    path('list-user', ListUserListCreate.as_view(), name='list_user_list'),
    path('list-user/<slug:slug>', ListUserGetUpdateDelete.as_view(),
         name='list_user_details'),
]
