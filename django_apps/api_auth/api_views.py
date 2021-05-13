from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response

from django_apps.api_auth.models import AccessToken
from django_apps.users.models import User


@api_view(['POST'])
def token(request):
    if request.method == 'POST':
        error = None
        header_keys = request.headers.keys()
        if 'username' not in header_keys:
            error = 'username missing from header.'
        elif 'password' not in header_keys:
            error = 'password missing from header.'
        if error:
            return Response({'status_code': 401, 'detail': error})
        username = request.headers['username']
        password = request.headers['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            access_token = AccessToken()
            token = access_token.generate_token(user.id)
            return Response({'status_code': 200, 'token': token})
        else:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                return Response({'status_code': 401, 'detail': 'Incorrect password. Try again.'})
            return Response({'status_code': 404, 'detail': 'User not found'})
