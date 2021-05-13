from rest_framework.generics import ListAPIView

from django_apps.users.serializers import UserSerializer
from django_apps.users.models import User

from django_apps.api_auth.authentication import APIAuthentication
from django_apps.api_auth.permissions import APIIsAuthenticated


class UserList(ListAPIView):
    authentication_classes = (APIAuthentication, )
    # permission_classes = (APIIsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
