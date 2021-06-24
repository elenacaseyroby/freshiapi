from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response

from django_apps.api_auth.models import AccessToken
from django_apps.api_auth.auth_utils import get_access_token
from django_apps.accounts.models import User


@api_view(['POST', ])
def token(request):
    if request.method == 'POST':
        error = None
        header_keys = request.headers.keys()
        if 'username' not in header_keys:
            error = 'username missing from header.'
        elif 'password' not in header_keys:
            error = 'password missing from header.'
        if error:
            return Response({
                'status_code': 401,
                'detail': error
            })
        # Usernames are stored in lowercase form, so make sure to inforce case here.
        username = request.headers['username'].lower()
        password = request.headers['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            access_token = AccessToken()
            token = access_token.generate_token(user.id)
            return Response({
                'status_code': 200,
                'detail': 'Success',
                'token': token,
                'user_id': user.id
            })
        else:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                return Response({
                    'status_code': 401,
                    'detail': 'Incorrect password. Try again.'
                })
            return Response({
                'status_code': 404,
                'detail': 'User not found'
            })


@api_view(['POST', ])
def revoke(request):
    if request.method == 'POST':
        if 'Authorization' not in request.headers.keys():
            return Response({
                'status_code': 401,
                'detail': 'Authorization token missing from the header'
            })
        token = request.headers['Authorization']
        try:
            access_token = get_access_token(token)
            access_token.revoke()
            return Response({
                'status_code': 200,
                'detail': 'Token successfully revoked'
            })
        except:
            return Response({
                'status_code': 200,
                'detail': 'Nothing executed. Token was already invalid'
            })
