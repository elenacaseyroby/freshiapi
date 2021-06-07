from rest_framework import exceptions

from datetime import date
import jwt

from django_apps.api_auth.models import AccessToken
from backend.settings import FRESHI_AUTH_ACCESS_KEY


def get_access_token(token):
    '''Input: token
    Output: user object if token is valid, false if token is invalid.'''
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
        code=code, user_id=user_id).first()
    # If expiration date is in future, token is valid
    # return user id
    if (
        access_token and
        access_token.expiration_date > date.today()
    ):
        return access_token
