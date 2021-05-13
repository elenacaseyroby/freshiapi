from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from django_apps.api_auth.auth_utils import get_access_token


class APIAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers['Authorization']
        if not token:  # no username passed in request headers
            raise exceptions.AuthenticationFailed(
                'Authorization token not in header')
        try:
            access_token = get_access_token(token)
            # BaseAuthentication class must return (user, None)
            # Then it checks user.is_authenticated to authenticate
            return (access_token.user, None)
        except:
            # raise exception if user does not exist
            raise exceptions.AuthenticationFailed(
                'Authorization token invalid')
