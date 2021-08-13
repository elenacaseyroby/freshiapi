from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_apps.accounts.custom_fields import CustomEmailField, CustomUsernameField


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
        db_table = 'accounts_users'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)


class PrivacyPolicy(models.Model):
    body = models.TextField(blank=False, null=False)
    date_published = models.DateField(
        blank=False, null=False)

    # object label in admin
    def __str__(self):
        return self.date_published

    class Meta:
        db_table = 'accounts_privacy_policies'


class Terms(models.Model):
    body = models.TextField(blank=False, null=False)
    date_published = models.DateField(
        blank=False, null=False)

    # object label in admin
    def __str__(self):
        return self.date_published

    class Meta:
        db_table = 'accounts_terms'


class UserTerms(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id')
    terms = models.ForeignKey(
        Terms, on_delete=models.CASCADE, db_column='terms_id')
    date_agreed = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)

    unique_together = [['user', 'terms']]

    class Meta:
        db_table = 'accounts_user_terms'


class UserPolicy(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id')
    policy = models.ForeignKey(
        PrivacyPolicy, on_delete=models.CASCADE, db_column='policy_id')
    date_agreed = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)

    unique_together = [['user', 'policy']]

    class Meta:
        db_table = 'accounts_user_policies'
