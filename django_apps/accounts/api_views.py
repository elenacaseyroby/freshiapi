from logging import error
from django.utils.functional import classproperty
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    CreateAPIView)
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from rest_framework.decorators import api_view

from django_apps.accounts.serializers import UserSerializer
from django_apps.accounts.models import User
from django_apps.api_auth.authentication import APIAuthentication
from django_apps.api_auth.auth_utils import get_access_token


@api_view(['POST', ])
def password_reset_email(request):
    if request.method == 'POST':
        if 'email' not in request.headers.keys():
            return Response({
                'status_code': 401,
                'detail': 'Email missing from the header'
            })
        email = request.headers['email']
        user = User.objects.filter(email=email).first()
        # Return error if there is no account under that email.
        if not user:
            return Response({
                'status_code': 401,
                'detail': 'There is no account tied to the email:  ' + email + '.'
            })
        # Make token.
        token = "alksfjlkajsf"  # placeholder
        try:
            # Send email.
            host = "localhost:8000"
            # host = "www.freshi.io"
            pw_reset_url = "{host}/reset-password/{user.id}/{token}"
            connection = get_connection(
                use_tls=settings.EMAIL_USE_TLS,
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD)
            subject = "Freshi Password Reset"
            body = "Hi {user.name}, \
                \
                Sorry to hear you're locked out of your account! Click <a href='{pw_reset_url}'>here</a> to reset your password.\
                \
                Please don't hesitate to reach out if you need any further help.\
                \
                take care,\
                \
                Casey\
                Cofounder of Freshi"
            EmailMessage(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [email, ],
                connection=connection).send()
            # Record in email db.
            return Response({
                'status_code': 200,
                'detail': 'Password reset email sent.'
            })
        except Exception as e:
            return Response({
                'status_code': 500,
                'detail': 'Email failed: ' + str(e)
            })


def formatError(errorField, errorMessage):
    return {
        "error_field": errorField,
        "error_message": errorMessage
    }


def getPasswordErrors(password):
    # return dict or None
    if not password:
        return formatError(
            "password",
            "Password must be set.")
    if len(password) < 8:
        return formatError(
            "password",
            "Password too short. Please enter a longer password.")
    if len(password) > 150:
        return formatError(
            "password",
            "Password too long. Please enter a shorter password.")


def savePasswordFromRequest(request, user):
    # Check if password passed in request.
    if "password" in request.data.keys():
        password = request.data.get("password")
        # Validate new password.
        passwordError = getPasswordErrors(password)
        if passwordError:
            raise ValidationError(passwordError, code=400)
        # Update password if no valdiation errors.
        user.set_password(password)
        user.save()


def userToUpdateMatchesLoggedInUser(request, user_to_update):
    token = request.headers['Authorization']
    access_token = get_access_token(token)
    logged_in_user = access_token.user
    # Only update if logged in user is same as the user being updated.
    if user_to_update.id != logged_in_user.id:
        return False
    return True


class UserCreate(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # If request is successful, set password:
        if (
            response.status_code >= 200 and
            response.status_code < 300
        ):
            email = request.data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                savePasswordFromRequest(request, user)
        return response


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    # Must prove logged in by passing Authentication token in header.
    authentication_classes = (APIAuthentication, )
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer

    # override update method
    def update(self, request, *args, **kwargs):
        # Get instance of user that will be updated.
        instance = self.get_object()

        # Get user associated with auth token used to authenticate request.
        if not userToUpdateMatchesLoggedInUser(request, instance):
            raise AuthenticationFailed(
                "Authorization error: You cannot update another user's account.")

        # Save password or throw error.
        savePasswordFromRequest(request, instance)

        # Update any attributes that were passed in the request.
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update cache.
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # Return serialized user.
        return Response(serializer.data)
