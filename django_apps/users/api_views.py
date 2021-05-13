from rest_framework.generics import ListAPIView

from django_apps.users.serializers import UserSerializer
from django_apps.users.models import User

from rest_framework.permissions import IsAuthenticated


class UserList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
