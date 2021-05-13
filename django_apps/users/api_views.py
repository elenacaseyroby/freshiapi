from rest_framework.generics import ListAPIView

from django_apps.users.serializers import UserSerializer
from django_apps.users.models import User

from django_apps.api_auth.authentication import APIAuthentication


class UserList(ListAPIView):
    # Must prove logged in by passing Authentication token in header.
    authentication_classes = (APIAuthentication, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
