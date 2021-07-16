from logging import error
from django.utils.functional import classproperty
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    CreateAPIView)
from rest_framework.response import Response
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    Throttled,
    ErrorDetail
)
from rest_framework.decorators import api_view
from django.conf import settings
from datetime import date

from django_apps.accounts.serializers import UserSerializer
from django_apps.accounts.models import User
from django_apps.api_auth.models import AccessToken
from django_apps.api_auth.authentication import APIAuthentication
from django_apps.api_auth.auth_utils import get_access_token
from django_apps.communications.services import send_email


@api_view(['POST', ])
def password_reset_email(request):
    if request.method == 'POST':
        if 'email' not in request.headers.keys():
            raise ValidationError(
                'Email missing from the header',
                code=401
            )
        email = request.headers['email']
        user = User.objects.filter(email=email).first()
        # Return error if there is no account under that email.
        if not user:
            raise ValidationError(
                'There is no account tied to the email:  ' + email + '.',
                code=401
            )

        pw_reset_attemps_today = AccessToken.objects.filter(
            user_id=user.id,
            date_created=date.today(),
            purpose='pw_reset',
        ).count()

        if pw_reset_attemps_today >= 3:
            raise Throttled(
                detail="""
You have reached your max number of password reset requests 
for the day. Please email casey@freshi.io for further help on this matter.""",
                code=401
            )

        # Make token.
        access_token = AccessToken()
        purpose = 'pw_reset'
        token = access_token.generate_token(user.id, purpose)

        # Send email.
        host = settings.FRESHI_URL
        # host = "www.freshi.io"
        pw_reset_url = f"http://{host}/reset-password/{user.id}/{token}"
        subject = "Freshi Password Reset"
        message = f"""Hi {user.first_name},

I'm sorry to hear you're locked out of your account! Visit {pw_reset_url} to reset your password.

If that doesn't do the trick, you can reply to this email and I'll be happy to provide further assistance.

Take care,

Casey

Co-founder of Freshi
        """
        html_message = f"""<!DOCTYPE html>
<html>
<head>
</head>
<body>
<p>Hi {user.first_name},</p>

<p>I'm sorry to hear you're locked out of your account! Click <a href='{pw_reset_url}'>here</a> to reset your password.</p>

<p>If that doesn't do the trick, you can reply to this email and I'll be happy to provide further assistance.</p>

<p>Take care,</p>

<p>Casey</p>

<p>Co-founder of Freshi</p>
</body>
</html>
        """

        # Send email, record in db, and return response.
        response = send_email(
            subject,
            message,
            settings.FRESHI_SUPPORT_EMAIL,
            [user.email],
            html_message=html_message)
        if response['status_code'] == 500:
            raise ErrorDetail(
                response['detail'],
                code=response['status_code'],
            )
        return Response(response)


@api_view(['POST', ])
def password_reset(request):
    if request.method == 'POST':
        api_authentification = APIAuthentication()
        user = api_authentification.authenticate(request)
        if not user:
            raise AuthenticationFailed(
                detail='Password reset token invalid.  Please request a new password reset email.',
                code=401
            )
        if "password" in request.data.keys():
            # Save new password
            savePasswordFromRequest(request, user)
            active_tokens = AccessToken.objects.filter(
                user_id=user.id,
                # active
                expiration_date__gt=date.today()
            ).all()

            # Deactivate all active access tokens.
            for token in active_tokens:
                token.expiration_date = date.today()
            AccessToken.objects.bulk_update(active_tokens, ['expiration_date'])
        else:
            raise ValidationError(
                'Password missing from header.',
                code=401
            )


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
                detail="Authorization error: You cannot update another user's account.",
                code=401
            )

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
