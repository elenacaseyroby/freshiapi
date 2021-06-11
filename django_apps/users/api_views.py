from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView)
from rest_framework.response import Response

from django_apps.users.serializers import UserSerializer
from django_apps.users.models import User

from django_apps.api_auth.authentication import APIAuthentication


class UserList(ListAPIView):
    # Must prove logged in by passing Authentication token in header.
    authentication_classes = (APIAuthentication, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRUD(RetrieveUpdateDestroyAPIView):
    # Must prove logged in by passing Authentication token in header.
    authentication_classes = (APIAuthentication, )
    serializer_class = UserSerializer


class UserCreate(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        # create user using custom user manager.
        user = User.objects.create_user(
            username, email, password, *args, **kwargs)
        # serialize response.
        serialized_user_data = UserSerializer(user).data
        return Response(serialized_user_data)
