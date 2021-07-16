from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
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
            raise ValidationError(
                error,
                code=401
            )
        # Usernames are stored in lowercase form, so make sure to inforce case here.
        username = request.headers['username'].lower()
        password = request.headers['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            access_token = AccessToken()
            purpose = 'login'
            token = access_token.generate_token(user.id, purpose)
            return Response({
                'status_code': 200,
                'detail': 'Success',
                'token': token,
                'user_id': user.id
            })
        else:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                raise ValidationError(
                    'Incorrect password. Try again.',
                    code=401
                )

            raise NotFound(
                detail='User not found',
                code=404
            )


@api_view(['POST', ])
def revoke(request):
    if request.method == 'POST':
        if 'Authorization' not in request.headers.keys():
            raise ValidationError(
                'Authorization token missing from the header',
                code=401
            )
        token = request.headers['Authorization']
        try:
            access_token = get_access_token(token)
            access_token.revoke()
            raise Response({
                'status_code': 200,
                'detail': 'Token successfully revoked'
            })
        except:
            raise Response({
                'status_code': 200,
                'detail': 'Nothing executed. Token was already invalid'
            })
