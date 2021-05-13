from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView)

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
    # Must prove logged in by passing Authentication token in header.
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            if username is None or len(username) < 3:
                raise ValidationError(
                    {'username': 'Username must be at least 3 characters in length'})
        except ValueError:
            raise ValidationError({
                'username': 'Please enter valid username'
            })
        try:
            password = request.data.get('password')
            if password is None or len(password) < 8:
                raise ValidationError(
                    {'password': 'Password must be at least 8 characters in length'}
                )
        except ValueError:
            raise ValidationError({
                'password': 'Please enter valid password'
            })
        try:
            email = request.data.get('email')
            if (
                email is None or
                '@' not in email or
                len(email) < 5
            ):
                raise ValidationError(
                    {'email': 'Email must be valid'}
                )
        except ValueError:
            raise ValidationError({
                'email': 'Please enter valid email'
            })
        try:
            first_name = request.data.get('first_name')
            if first_name is None or len(first_name) < 2:
                raise ValidationError(
                    {'first_name': 'First name must be at least 2 characters in length'}
                )
        except ValueError:
            raise ValidationError({
                'first_name': 'Please enter valid first name'
            })
        try:
            last_name = request.data.get('last_name')
            if last_name is None or len(last_name) < 2:
                raise ValidationError(
                    {'last_name': 'Last name must be at least 2 characters in length'}
                )
        except ValueError:
            raise ValidationError({
                'last_name': 'Please enter valid last name'
            })
        return super().create(request, *args, **kwargs)
