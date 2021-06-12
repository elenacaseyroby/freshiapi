from django.contrib.auth.models import BaseUserManager
from rest_framework.exceptions import ValidationError
# from django_apps.users.models import User


def formatError(errorField, errorMessage):
    return {
        "error_field": errorField,
        "error_message": errorMessage
    }


def getEmailErrors(user_objects, email):
    # return dict or None
    if not email:
        return formatError(
            "email",
            "Email must be set.")
    if (
        len(email) < 5 or
        '@' not in email
    ):
        return formatError(
            "email",
            "Please enter valid email.")
    if len(email) > 255:
        return formatError(
            "email",
            "Email too long. Please enter shorter email.")
    if " " in email.strip():
        return formatError(
            "email",
            "Email cannot contain spaces.")
    if user_objects.filter(email=email).count() > 0:
        return formatError(
            "email",
            "A user with that email address already exists.")
    return None


def getUsernameErrors(user_objects, username):
    # return dict or None
    if not username:
        return formatError(
            "username",
            "Username must be set.")
    if len(username) < 3:
        return formatError(
            "username",
            "Username too short. Please enter a longer username.")
    if len(username) > 150:
        return formatError(
            "username",
            "Username too long.  Please enter a shorter username.")
    if " " in username.strip():
        return formatError(
            "username",
            "Username cannot contain spaces.")
    if user_objects.filter(username=username).count() > 0:
        return formatError(
            "username",
            "A user with that username already exists.")
    return None


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


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        error = getEmailErrors(self, email)
        if not error:
            error = getUsernameErrors(self, username)
        if not error:
            error = getPasswordErrors(password)
        if error:
            raise ValidationError(error)
        # By default, username and email are unique but case sensitive.
        # To make sure that "Casey" and "casey" are treated the same,
        # we will make username and email lowercase before saving.
        email = email.lower().strip()
        username = username.lower().strip()
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)
