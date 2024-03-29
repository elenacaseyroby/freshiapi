from rest_framework import exceptions

from django.utils import timezone
import jwt

from django_apps.api_auth.models import AccessToken
from backend.settings import FRESHI_AUTH_ACCESS_KEY


def get_access_token(token):
    '''Input: token
    Output: user object if token is valid, None if token is invalid.'''
    try:
        payload = jwt.decode(
            token,
            FRESHI_AUTH_ACCESS_KEY,
            algorithms="HS256"
        )
    except:
        raise exceptions.ErrorDetail("Unable to decode token.")
    user_id = payload['user_id']
    code = payload['code']
    access_token = AccessToken.objects.filter(
        code=code,
        user_id=user_id,
        expiration_time__gt=timezone.now()).first()
    return access_token
