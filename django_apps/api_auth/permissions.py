from rest_framework.permissions import BasePermission
from rest_framework import exceptions

from django_apps.api_auth.auth_utils import get_access_token


class APIIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # Return true or raise auth failed error.
        token = request.headers['Authorization']
        if not token:  # no username passed in request headers
            raise exceptions.AuthenticationFailed(
                'Authorization token not in header')
        try:
            access_token = get_access_token(token)
            # BaseAuthentication class must return (user, None)
            # Then it checks user.is_authenticated to authenticate
            if access_token:
                return True
        except:
            # raise exception if user does not exist
            raise exceptions.AuthenticationFailed(
                'Authorization token invalid')
