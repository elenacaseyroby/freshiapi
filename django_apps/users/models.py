from django.db import models
from django.contrib.auth.models import AbstractUser
from django_apps.users.custom_fields import CustomEmailField, CustomUsernameField


class User(AbstractUser):
    # AbstractBaseUser provides the core implementation of a user model,
    # including hashed passwords and tokenized password resets.
    # AbstractUser provides authentication ^^ plus extra fields like
    # first_name, last_name, etc.
    email = CustomEmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    username = CustomUsernameField(
        verbose_name='Username',
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    # username 150, unique
    # first_name 150
    # last_name 150
    # updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    # A list of the field names that will be prompted for when creating
    # a user via the createsuperuser.
    # Has no bearing on creation of user in other contexts.
    # username, email and password are required by default
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = '"users_users"'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
