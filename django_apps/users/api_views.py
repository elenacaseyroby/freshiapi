from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView)
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_apps.users.serializers import UserSerializer
from django_apps.users.models import User
from django_apps.api_auth.auth_utils import get_access_token

from django_apps.api_auth.authentication import APIAuthentication


# class UserList(ListAPIView):

#     authentication_classes = (APIAuthentication, )
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


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


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    # Must prove logged in by passing Authentication token in header.
    authentication_classes = (APIAuthentication, )
    # make sure that userId from auth is the only user that can be updated.
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer

    # override update method
    def update(self, request, *args, **kwargs):
        # Get user associated with auth token used to authenticate request.
        token = request.headers['Authorization']
        access_token = get_access_token(token)
        logged_in_user = access_token.user
        user_to_update = self.get_object()
        if user_to_update.id != logged_in_user.id:
            raise AuthenticationFailed(
                'Authorization error: Authorization token invalid')
        response = super().update(request, *args, **kwargs)
        # If password is passed, update that too:
        if "password" in request.data.keys():
            password = request.data.get("password")
            logged_in_user.set_password(password)
            logged_in_user.save()
        # if successfully updates, update cache
        # if response.status_code == 200:
        #     from django.core.cache import cache
        #     user = response.data
        #     cache.set('user_data_{}'.format(user['id']), {
        #         'first_name': user['first_name'],
        #         'last_name': user['last_name'],
        #         'username': user['username'],
        #         'email': user['email'],
        #     })
        return response

        # def delete(self, request, *args, **kwargs):  # override delete method
    #     product_id = request.data.get('id')  # get id from request
    #     response = super().delete(request, *args, **kwargs)  # delete object
    #     # if object is successfully deleted, clear cache.
    #     if response.status_code == 200:
    #         from django.core.cache import cache
    #         cache.delete('product_data_{}'.format(product_id))
    #     return response
