from django.urls import path

from user import views

urlpatterns = [
    path('user-admin/', views.UserAdminListCreate.as_view(),
         name='user-admin-list'),
    path('user-admin/<str:username>', views.UserAdminGetUpdateDelete.as_view(),
         name='user-admin-details'),
    path('user-token/', views.CreateTokenView.as_view(),
         name='user-admin-token'),
    path('user-regular/', views.UserGetUpdateDelete.as_view(),
         name='user-regular-list'),
]
