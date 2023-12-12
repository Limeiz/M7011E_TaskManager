from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth.models import User

from catalog.views import IsAdmin, IsRegularUser
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class UserViewSet(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]


class UserAdminListCreate(UserViewSet, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class UserAdminGetUpdateDelete(UserViewSet,
                               generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'username'


class UserGetUpdateDelete(UserViewSet, generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
